import json
from time        import time
from datetime    import datetime
from pathlib     import Path
from collections import defaultdict

from dotmng.modules import log_manager

from dotmng.modules.database.models  import *

from sqlalchemy                  import create_engine, event, Engine, func, select, case, literal
from sqlalchemy.orm              import sessionmaker, aliased
from sqlalchemy.dialects.sqlite  import insert


class DataBase:
    def __init__(self, base_path: Path):
        self.log = log_manager.setup_logger("DB")
        self.db_path = base_path

        # Configuración de la base de datos SQLite
        sqlite = f"sqlite:///{self.db_path}"
        self.engine = create_engine(sqlite)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

        # Registra las consultas SQL
        @event.listens_for(Engine, "before_cursor_execute")
        def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
            conn.info.setdefault('query_start_time', []).append(time())
            self.log.debug(f"Ejecutando SQL: {statement} | Parámetros: {parameters}")

        @event.listens_for(Engine, "after_cursor_execute")
        def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
            # Recuperamos el tiempo y calculamos el total
            total = time() - conn.info['query_start_time'].pop()
            self.log.debug(f"Consulta completada en {total:.3f}s.")

        # Asegura que las tablas estén creadas
        Base.metadata.create_all(bind=self.engine)

        # Comprueba si es necesario el seed automático
        session = self.SessionLocal()
        needs_seed = False

        try:
            if session.query(KnownAppsReference).first() is None:
                needs_seed = True

        except Exception:
            pass

        finally:
            session.close()

        if needs_seed:
            self.log.warning(f"Ejecutando seed de datos por defecto...")
            from dotmng.data.db_init import initialize_database
            initialize_database(self)

        self.log.info(f"Base de datos iniciada.")

    def is_first_run(self) -> bool:
        """
        Devuelve True si local_inventory está vacía.
        Indica que nunca se ha ejecutado 'update' en este equipo.
        """
        session = self.SessionLocal()
        try:
            return session.query(LocalInventory).first() is None
        except Exception:
            return True
        finally:
            session.close()

    def get_conf_server(self, config:str):
        session = self.SessionLocal()
        try:
            self.log.debug(f"Recuperando valor {config}")
            result = session.query(ServerConfig).filter_by(key=config).first()
            return result.value if result else None

        except Exception as e:
            self.log.error(e)
            raise e

        finally:
            session.close()

    def set_conf_server(self, config, value):
        session = self.SessionLocal()
        try:
            self.log.debug(f"Actualizando {config}...")
            
            if value == "now":
                # Formato: %d / %m / %Y   %H:%M:%S (3 espacios antes de %H)
                value = datetime.now().strftime("%d / %m / %Y   %H:%M:%S")

            # Intentamos recuperar para ver si existe
            entry = session.query(ServerConfig).filter_by(key=config).first()
            
            if entry:
                entry.value = str(value)
            else:
                new_entry = ServerConfig(key=config, value=str(value))
                session.add(new_entry)
            
            session.commit()
            return value

        except Exception as e:
            session.rollback()
            self.log.error(e)
            raise e

        finally:
            session.close()

    def get_categories_app(self, category: str = None, parent_id: int = None, session=None):
        _session = session or self.SessionLocal()
        try:
            if category:
                self.log.debug(f"Buscando categoría: '{category}' (parent: {parent_id})")
                query = _session.query(CategoriesApps).filter_by(category=category)
                
                if parent_id is not None:
                    query = query.filter_by(parent_id=parent_id)

                category_obj = query.first()

                if category_obj:
                    return category_obj.to_dict()

            return None

        except Exception as e:
            if not session: _session.rollback()
            self.log.error(e)
            raise e

        finally:
            if not session: _session.close()

    def set_categories(self, category: str, parent_id: int=None, session=None):
        _session = session or self.SessionLocal()
        try:
            if not category:
                return None

            category_obj = CategoriesApps(
                category=category,
                parent_id=parent_id
            )

            _session.add(category_obj)
            
            if not session:
                _session.commit()
            else:
                _session.flush()

            self.log.debug(f"Agregada [{category_obj.category}] con id: {category_obj.id_cat}")
            return category_obj.id_cat

        except Exception as e:
            if not session: _session.rollback()
            self.log.error(e)
            raise e

        finally:
            if not session: _session.close()

    def del_categories(self, category: str=None, parent_id: int=None):
        session = self.SessionLocal()
        try:
            if category:
                self.log.info(f"Eliminando categoría: {category}")
                session.query(CategoriesApps).filter_by(
                    category=category
                ).delete()
                session.commit()

            if parent_id:
                self.log.info(f"Eliminando categoría on id: {parent_id}")
                session.query(CategoriesApps).filter_by(
                    id_cat=parent_id
                ).delete()
                session.commit()

        except Exception as e:
            session.rollback()
            self.log.error(e)

        finally:
            session.close()

    def get_known_apps(self):
        session = self.SessionLocal()
        try:
            self.log.debug(f"Recuperando aplicaciones conocidas de la BD")
            return session.query(KnownAppsReference).all()

        except Exception as e:
            self.log.error(e)
            session.rollback()
            raise e

        finally:
            session.close()

    def get_file_info_known_apps(self):
        session = self.SessionLocal()
        try:
            self.log.debug(f"Recuperando file_info de aplicaciones conocidas...")
            return session.query(
                KnownAppsReference.app_id,
                KnownAppsReference.files_info_json
            ).all()

        except Exception as e:
            self.log.error(e)
            raise e

        finally:
            session.close()

    def set_known_apps(self, data, session=None):
        _session = session or self.SessionLocal()
        try:
            self.log.info(f"Agregando o actualizando {len(data)} aplicaciones conocidas...")
            for d in data:
                # session.merge se encarga de hacer un INSERT o UPDATE según la clave primaria
                _session.merge(d)
            
            if not session:
                _session.commit()
                self.log.info("Aplicaciones conocidas guardadas correctamente.")

        except Exception as e:
            if not session: _session.rollback()
            self.log.error(f"Error al guardar aplicaciones conocidas: {e}")
            raise e

        finally:
            if not session: _session.close()

    def save_classified_data(self, data: dict):
        session = self.SessionLocal()
        try:
            apps_to_save = []
            for app_id, details in data.items():
                try:
                    # Omitir si la aplicación es desconocida o está marcada para ser ignorada
                    if details.get('app_name') == 'Unknown' or details.get('ignored') is True:
                        self.log.info(f"Omitiendo guardar app '{app_id}' porque está marcada como 'Unknown' o 'ignored'.")
                        continue

                    # 1. Gestionar categoría padre
                    p_cat = self.get_categories_app(details['category'], session=session)
                    p_id = p_cat['id_cat'] if p_cat else self.set_categories(details['category'], session=session)

                    # 2. Gestionar subcategoría
                    s_id = None
                    if details.get('subcategory'):
                        s_cat = self.get_categories_app(details['subcategory'], session=session)
                        s_id = s_cat['id_cat'] if s_cat else self.set_categories(details['subcategory'], parent_id=p_id, session=session)

                    if not s_id:
                        s_id = p_id

                    # 3. Preparar el objeto para guardar
                    apps_to_save.append(KnownAppsReference(
                        app_id=app_id,
                        app_name=details['app_name'],
                        category_id=s_id,
                        files_info_json=json.dumps(details['files_info_json']),
                        packages_json=json.dumps(details['packages_json']),
                    ))

                except Exception as e:
                    self.log.error(f"Error procesando la app '{app_id}' durante la clasificación: {e}")

            if apps_to_save:
                self.set_known_apps(apps_to_save, session=session)
                session.commit()
                self.log.info(f"Guardado final de {len(apps_to_save)} aplicaciones clasificados.")
            else:
                self.log.warning("No se procesaron aplicaciones para guardar.")

        except Exception as e:
            self.log.error(f"Error en la transacción de guardado de datos clasificados: {e}")
            session.rollback()
        finally:
            session.close()

    def get_global_ignore_rules(self):
        session = self.SessionLocal()
        try:
            self.log.debug(f"Recuperando reglas de exclusión global...")

            # LEFT JOIN con user_ignore_overrides para calcular enabled efectivo.
            # Si no hay override del usuario → habilitado por defecto (True).
            stmt = select(
                GlobalIgnoreRules.id,
                GlobalIgnoreRules.pattern,
                GlobalIgnoreRules.match_type,
                case(
                    (UserIgnoreOverrides.id.is_(None), literal(True)),
                    else_=UserIgnoreOverrides.enabled
                ).label("enabled")
            ).outerjoin(
                UserIgnoreOverrides,
                GlobalIgnoreRules.id == UserIgnoreOverrides.rule_id
            )

            results = session.execute(stmt).all()

            grouped_data = {}
            for row in results:
                grouped_data[row.id] = {
                    "enabled": row.enabled,
                    "match_type": row.match_type,
                    "pattern": row.pattern
                }

            return grouped_data

        except Exception as e:
            self.log.error(e)
            raise e

        finally:
            session.close()

    def set_global_ignore_rules(self, data):
        session = self.SessionLocal()
        try:
            for d in data:
                session.merge(d)

            self.log.info(f"Actualizadas {len(data)} reglas de exclusión globales en la BD.")
            session.commit()

        except Exception as e:
            session.rollback()
            self.log.error(e)
            raise e

        finally:
            session.close()

    def get_local_for_inform(self):
        session = self.SessionLocal()
        try:
            father_cat = aliased(CategoriesApps)
            son_cat = aliased(CategoriesApps)

            stmt = select(
                father_cat.category.label("parent"),
                son_cat.category.label("sub"),
                KnownAppsReference.app_name,
                LocalInventory.path,
                LocalInventory.app_id
            ).join(
                KnownAppsReference, LocalInventory.app_id == KnownAppsReference.app_id
            ).join(
                son_cat, KnownAppsReference.category_id == son_cat.id_cat
            ).outerjoin(
                father_cat, son_cat.parent_id == father_cat.id_cat
            ).order_by("parent", "sub", KnownAppsReference.app_name)

            results = session.execute(stmt).all()

            grouped_data = defaultdict(lambda: defaultdict(list))
            for row in results:
                parent = row.parent
                name = row.app_name
                sub = row.sub
                app_id = row.app_id
                path = row.path
                grouped_data[parent][(name, sub, app_id)].append(path)

            return dict(grouped_data)

        except Exception as e:
            self.log.error(e)
            raise e

        finally:
            session.close()

    def get_local_conflicts(self):
        session = self.SessionLocal()
        try:
            # 1. Obtenemos los app_id que el usuario ha deshabilitado explícitamente
            disabled_apps_stmt = select(UserInventoryOverrides.app_id).where(
                UserInventoryOverrides.enabled == False
            )

            # 2. Buscamos paths con colisiones (más de 1 app),
            # excluyendo las que el usuario deshabilitó
            stmt_sub = select(LocalInventory.path).where(
                LocalInventory.app_id.not_in(disabled_apps_stmt)
            ).group_by(
                LocalInventory.path
            ).having(
                func.count(LocalInventory.path) > 1
            )

            # 3. Datos completos de los paths conflictivos
            stmt_main = select(
                LocalInventory,
                KnownAppsReference.app_name
            ).join(
                KnownAppsReference,
                LocalInventory.app_id == KnownAppsReference.app_id
            ).where(
                LocalInventory.path.in_(stmt_sub),
                LocalInventory.app_id.not_in(disabled_apps_stmt)
            ).order_by(
                LocalInventory.path
            )

            results = session.execute(stmt_main).all()

            # 4. Salida agrupada por path
            grouped_conflicts = defaultdict(list)
            for item, app_name in results:
                grouped_conflicts[item.path].append({
                    "id": item.id,
                    "app_id": item.app_id,
                    "app_name": app_name,
                    "type": item.type
                })

            return dict(grouped_conflicts)

        except Exception as e:
            self.log.error(e)
            raise e

        finally:
            session.close()

    def get_local_inventory(self):
        session = self.SessionLocal()
        try:
            self.log.debug(f"Recuperando inventario local...")

            results = session.query(LocalInventory).all()
            grouped_apps = {}
            for app in results:
                grouped_apps[app.id] = {
                    "path": app.path,
                    "type": app.type,
                    "app_id": app.app_id
                }

            return grouped_apps

        except Exception as e:
            self.log.error(e)
            raise e

        finally:
            session.close()

    def get_local_inventory_by_id(self, id):
        session = self.SessionLocal()
        try:
            self.log.debug(f"Recuperando app local por id: {id}...")

            stmt = select(LocalInventory).filter_by(id=id)
            result = session.execute(stmt).scalar_one_or_none()

            if not result:
                return None

            return {
                "id": result.id,
                "path": result.path,
                "type": result.type,
                "app_id": result.app_id,
            }

        except Exception as e:
            self.log.error(e)
            raise e

        finally:
            session.close()

    def set_local_inventory(self, data):
        session = self.SessionLocal()
        try:
            self.log.info(f"Limpiando tabla {LocalInventory.__tablename__}...")
            session.query(LocalInventory).delete()

            local_inventory = []
            for d in data:
                new_app = LocalInventory(
                    path=d["path"],
                    type=d["type"],
                    app_id=d["app_id"]
                )
                session.add(new_app)
                local_inventory.append(new_app)

            session.commit()
            self.log.info(f"Inventario local actualizado con éxito: {len(data)} archivos agregados/modificados.")

            for app in local_inventory:
                session.refresh(app)

            return local_inventory

        except Exception as e:
            session.rollback()
            self.log.error(e)
            raise e

        finally:
            session.close()

    def del_local_inventory_by_id(self, id_app):
        session = self.SessionLocal()

        try:
            session.query(LocalInventory).filter_by(id=id_app).delete()
            session.commit()

            self.log.info(f"Eliminado app con id: {id_app}")

        except Exception as e:
            session.rollback()
            self.log.error(e)
            raise e

        finally:
            session.close()

    def clear_local_inventory_and_unknown(self):
        session = self.SessionLocal()
        try:
            self.log.info("Limpiando tablas local_inventory, local_unknown y system_state_hashes para reescaneo...")
            session.query(LocalInventory).delete()
            session.query(LocalUnknown).delete()
            session.query(SystemStateHashes).delete()
            session.commit()
            self.log.info("Tablas locales limpiadas con éxito.")
        except Exception as e:
            session.rollback()
            self.log.error(f"Error al limpiar tablas locales en la base de datos: {e}")
            raise e
        finally:
            session.close()


    def get_local_unknown(self):
        session = self.SessionLocal()
        try:
            self.log.debug(f"Recuperando inventario de archivos desconocidos...")

            # LEFT JOIN con user_unknown_overrides para calcular enabled efectivo.
            # Si no hay override del usuario → habilitado por defecto (True).
            stmt = select(
                LocalUnknown.id,
                LocalUnknown.path,
                LocalUnknown.type,
                case(
                    (UserUnknownOverrides.id.is_(None), literal(True)),
                    else_=UserUnknownOverrides.enabled
                ).label("enabled")
            ).outerjoin(
                UserUnknownOverrides,
                LocalUnknown.path == UserUnknownOverrides.path
            )

            results = session.execute(stmt).all()
            grouped_apps = {}
            for row in results:
                grouped_apps[row.id] = {
                    "path": row.path,
                    "type": row.type,
                    "enabled": row.enabled
                }

            return grouped_apps

        except Exception as e:
            self.log.error(e)
            raise e

        finally:
            session.close()

    def set_local_unknown(self, data):
        session = self.SessionLocal()
        try:
            self.log.info(f"Actualizando tabla {LocalUnknown.__tablename__} mediante upsert por path...")

            local_unknown = []
            for d in data:
                stmt = insert(LocalUnknown).values(
                    path=d["path"],
                    type=d["type"]
                )
                # UPSERT: si el path ya existe, solo actualiza type y last_seen
                stmt = stmt.on_conflict_do_update(
                    index_elements=['path'],
                    set_={
                        'type': stmt.excluded.type,
                        'last_seen': func.now()
                    }
                )
                session.execute(stmt)

            session.commit()
            self.log.info(f"Inventario de archivos desconocidos actualizado: {len(data)} registros (Upsert completado).")

            # Recuperar los objetos actualizados para devolverlos
            paths = [d["path"] for d in data]
            local_unknown = session.query(LocalUnknown).filter(
                LocalUnknown.path.in_(paths)
            ).all()

            for app in local_unknown:
                session.refresh(app)

            return local_unknown

        except Exception as e:
            session.rollback()
            self.log.error(e)
            raise e

        finally:
            session.close()

    def get_local_unknown_by_id(self, id_app: int) -> dict | None:
        """Devuelve el path y type de un archivo desconocido dado su id."""
        session = self.SessionLocal()
        try:
            result = session.query(LocalUnknown).filter_by(id=id_app).first()
            if not result:
                self.log.warning(f"No se encontró el archivo desconocido con id: {id_app}")
                return None
            return {"id": result.id, "path": result.path, "type": result.type}

        except Exception as e:
            self.log.error(e)
            raise e

        finally:
            session.close()

    def get_system_state_hashes(self, list_name):
        session = self.SessionLocal()
        try:
            self.log.debug(f"Recuperando hash de la lista '{list_name}'")
            data = session.query(SystemStateHashes).filter_by(list_name=list_name).first()
            if not data:
                return None

            return data

        except Exception as e:
            self.log.error(e)
            raise e

        finally:
            session.close()

    def set_system_state_hashes(self, hashed, count, list_name):
        session = self.SessionLocal()
        try:
            stmt = insert(SystemStateHashes).values(
                list_name=list_name,
                current_hash=hashed,
                item_count=count
            )

            stmt = stmt.on_conflict_do_update(
                index_elements=['list_name'],
                set_={
                    'current_hash': hashed,
                    'item_count': count,
                    'last_checked_at': datetime.now()
                },
            )

            session.execute(stmt)
            session.commit()

            self.log.info(f"Estado del sistema actualizado: Hash registrado para la lista '{list_name}' con {count} elementos.")

        except Exception as e:
            session.rollback()
            self.log.error(e)
            raise e

        finally:
            session.close()

    def get_user_inventory_overrides(self):
        """Devuelve los overrides del usuario sobre el inventario conocido.
        Solo contiene entradas donde el usuario cambió el estado por defecto.
        La clave es app_id, el valor indica si está habilitado.
        """
        session = self.SessionLocal()
        try:
            self.log.debug(f"Recuperando overrides del inventario...")
            results = session.query(UserInventoryOverrides).all()

            return {
                row.app_id: {
                    "enabled": row.enabled,
                    "last_changed_at": row.last_changed_at
                }
                for row in results
            }

        except Exception as e:
            self.log.error(e)
            raise e

        finally:
            session.close()

    def set_user_inventory_override(self, app_id: str, enabled: bool):
        """Upsert del override de usuario para una app del inventario conocido."""
        session = self.SessionLocal()
        try:
            stmt = insert(UserInventoryOverrides).values(
                app_id=app_id,
                enabled=enabled
            )

            stmt = stmt.on_conflict_do_update(
                index_elements=['app_id'],
                set_={
                    'enabled': stmt.excluded.enabled,
                    'last_changed_at': func.now()
                }
            )

            session.execute(stmt)
            session.commit()

            action = "Habilitado" if enabled else "Deshabilitado"
            self.log.info(f"Preferencia de usuario: {action} override para la app '{app_id}' en el inventario local.")

        except Exception as e:
            session.rollback()
            self.log.error(e)
            raise e

        finally:
            session.close()

    def set_user_unknown_override(self, path: str, enabled: bool):
        """Upsert del override de usuario para un archivo desconocido (por path)."""
        session = self.SessionLocal()
        try:
            stmt = insert(UserUnknownOverrides).values(
                path=path,
                enabled=enabled
            )

            stmt = stmt.on_conflict_do_update(
                index_elements=['path'],
                set_={
                    'enabled': stmt.excluded.enabled,
                    'last_changed_at': func.now()
                }
            )

            session.execute(stmt)
            session.commit()

            action = "Habilitado" if enabled else "Deshabilitado"
            self.log.info(f"Preferencia de usuario: {action} override para el path desconocido '{path}'.")

        except Exception as e:
            session.rollback()
            self.log.error(e)
            raise e

        finally:
            session.close()

    def set_user_ignore_override(self, rule_id: int, enabled: bool):
        """Upsert del override de usuario para una regla de exclusión global."""
        session = self.SessionLocal()
        try:
            stmt = insert(UserIgnoreOverrides).values(
                rule_id=rule_id,
                enabled=enabled
            )

            stmt = stmt.on_conflict_do_update(
                index_elements=['rule_id'],
                set_={
                    'enabled': stmt.excluded.enabled,
                    'last_changed_at': func.now()
                }
            )

            session.execute(stmt)
            session.commit()

            action = "Habilitado" if enabled else "Deshabilitado"
            self.log.info(f"Preferencia de usuario: {action} override para la regla de exclusión ID {rule_id}.")

        except Exception as e:
            session.rollback()
            self.log.error(e)
            raise e

        finally:
            session.close()

    def get_server_task(self, task_id: str=None):
        session = self.SessionLocal()
        try:
            if task_id:
                self.log.debug(f"Recuperando tarea con id: {task_id}")
                task = session.query(ServerTasks).filter_by(task_id=task_id).first()
                return task.to_dict() if task else None

            # Buscar alguna que esté en estado 'QUEUE' o 'PROCESSING'
            task = session.query(ServerTasks).filter(
                ServerTasks.state.in_(['QUEUE', 'PROCESSING'])
            ).order_by(ServerTasks.created_at.desc()).first()

            if task:
                self.log.debug(f"Recuperando tarea activa/pendiente: {task.task_id}")
                return task.to_dict()

            self.log.debug(f"No hay tareas activas/pendientes.")
            return None

        except Exception as e:
            self.log.error(e)
            raise e

        finally:
            session.close()

    def set_server_task(self, task_id: str, state: str=None):
        session = self.SessionLocal()
        try:
            # Si no se proporciona estado, usamos QUEUE por defecto
            if state is None:
                state = 'QUEUE'
            else:
                state = state.upper()

            stmt = insert(ServerTasks).values(
                task_id=task_id,
                state=state
            )

            stmt = stmt.on_conflict_do_update(
                index_elements=['task_id'],
                set_={
                    'state': stmt.excluded.state
                }
            )

            session.execute(stmt)
            session.commit()

            self.log.info(f"Actualizada tarea id: {task_id} con estado: {state}")

        except Exception as e:
            session.rollback()
            self.log.error(e)
            raise e

        finally:
            session.close()