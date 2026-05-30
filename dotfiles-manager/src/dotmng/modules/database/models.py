from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, CheckConstraint, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base()


# 1. PREFERENCIAS DE LA UI
class UI_Preferences(Base):
    __tablename__   = 'ui_preferences'
    id              = Column(Integer, primary_key=True, autoincrement=True)
    key             = Column(String, nullable=False, unique=True)
    value           = Column(String, nullable=False)
    update_at       = Column(DateTime, default=datetime.now, onupdate=datetime.now)


# 2. CONFIGURACIÓN DEL SERVIDOR Y EQUIPO
class ServerConfig(Base):
    __tablename__   = 'server_config'
    id              = Column(Integer, primary_key=True, autoincrement=True)
    key             = Column(String, nullable=False, unique=True)
    value           = Column(String, nullable=False)
    update_at       = Column(DateTime, default=datetime.now, onupdate=datetime.now)


# 3. MAPEADO DE SISTEMAS OPERATIVOS
class OSDistroMapping(Base):
    __tablename__   = 'os_distro_mapping'
    distro_id       = Column(String, primary_key=True)


# 4. CATEGORÍAS DE LAS APLICACIONES
class CategoriesApps(Base):
    __tablename__   = 'categories_apps'
    id_cat          = Column(Integer, primary_key=True, autoincrement=True)
    category        = Column(String, nullable=False, unique=True)
    parent_id       = Column(Integer, ForeignKey('categories_apps.id_cat'), nullable=True)

    # Relaciones
    app_reference   = relationship("KnownAppsReference", back_populates="category_ref")

    def to_dict(self):
        return {
            "id_cat": self.id_cat,
            "category": self.category,
            "parent_id": self.parent_id
        }


# 5. BASE DE DATOS LOCAL DE APLICACIONES CONOCIDAS
class KnownAppsReference(Base):
    __tablename__   = 'known_apps_reference'
    app_id          = Column(String, primary_key=True)
    app_name        = Column(String, nullable=False)
    category_id     = Column(Integer, ForeignKey('categories_apps.id_cat'), nullable=False)
    files_info_json = Column(String)
    packages_json   = Column(String)

    # Relaciones
    category_ref    = relationship("CategoriesApps", back_populates="app_reference")
    inventory_local = relationship("LocalInventory", back_populates="app")


# 6. REGLAS GLOBALES DE EXCLUSIÓN
class GlobalIgnoreRules(Base):
    __tablename__   = 'global_ignore_rules'
    id              = Column(Integer, primary_key=True, autoincrement=True)
    pattern         = Column(String, nullable=False)
    match_type      = Column(String, nullable=False)

    __table_args__  = (CheckConstraint(
            "match_type IN ('REGEX', 'EXACT', 'EXTENSION')",
            name='check_valid_match_type'
    ),)

    # Relaciones
    user_override   = relationship("UserIgnoreOverrides", back_populates="rule", uselist=False)


# 7. CACHÉ DEL INVENTARIO LOCAL (Lo escaneado en este equipo)
class LocalInventory(Base):
    __tablename__   = 'local_inventory'
    id              = Column(Integer, primary_key=True, autoincrement=True)
    path            = Column(String, nullable=False)
    type            = Column(String, nullable=False)
    app_id          = Column(String, ForeignKey('known_apps_reference.app_id'), nullable=False)
    last_seen       = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    __table_args__  = (CheckConstraint(
        "type IN ('file', 'folder')",
        name='check_valid_type'
    ),)

    # Relaciones
    app = relationship("KnownAppsReference", back_populates="inventory_local")


# 8. CACHÉ DEL INVENTARIO LOCAL DESCONOCIDO (Lo escaneado en este equipo)
class LocalUnknown(Base):
    __tablename__   = 'local_unknown'
    id              = Column(Integer, primary_key=True, autoincrement=True)
    path            = Column(String, nullable=False, unique=True)
    type            = Column(String, nullable=False)
    last_seen       = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    __table_args__  = (
        CheckConstraint(
            "type IN ('file', 'folder')",
            name='check_valid_type'
        ),
        UniqueConstraint('path', name='uq_local_unknown_path'),
    )

    # Relaciones
    user_override   = relationship("UserUnknownOverrides", back_populates="unknown_file",
                                   foreign_keys="UserUnknownOverrides.path",
                                   primaryjoin="LocalUnknown.path == UserUnknownOverrides.path",
                                   uselist=False)


# 9. HASHES DE LISTADOS DE LOS DOTFILES DEL USUARIO (Para detectar cambios en dotfiles)
class SystemStateHashes(Base):
    __tablename__   = 'system_state_hashes'
    id              = Column(Integer, primary_key=True, autoincrement=True)
    list_name       = Column(String, nullable=False, unique=True)
    current_hash    = Column(String, nullable=False)
    item_count      = Column(Integer, default=0, nullable=False)
    created_at      = Column(DateTime, default=datetime.now)
    last_checked_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    __table_args__  = (CheckConstraint(
            "list_name IN ('ALL_DOTFILES', 'KNOWNS', 'UNKNOWNS')",
            name='check_valid_list_name'
    ),)

    def str_hash(self):
        return str(self.current_hash)


# 10a. OVERRIDES DE USUARIO — Inventario Conocido
class UserInventoryOverrides(Base):
    __tablename__   = 'user_inventory_overrides'
    id              = Column(Integer, primary_key=True, autoincrement=True)
    app_id          = Column(String, ForeignKey('known_apps_reference.app_id'), nullable=False, unique=True)
    enabled         = Column(Boolean, nullable=False, default=False)
    last_changed_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    # Relaciones
    app             = relationship("KnownAppsReference")


# 10b. OVERRIDES DE USUARIO — Archivos Desconocidos
class UserUnknownOverrides(Base):
    __tablename__   = 'user_unknown_overrides'
    id              = Column(Integer, primary_key=True, autoincrement=True)
    path            = Column(String, ForeignKey('local_unknown.path'), nullable=False, unique=True)
    enabled         = Column(Boolean, nullable=False, default=False)
    last_changed_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    # Relaciones
    unknown_file    = relationship("LocalUnknown", back_populates="user_override",
                                   foreign_keys=[path],
                                   primaryjoin="UserUnknownOverrides.path == LocalUnknown.path")


# 10c. OVERRIDES DE USUARIO — Reglas de Exclusión Globales
class UserIgnoreOverrides(Base):
    __tablename__   = 'user_ignore_overrides'
    id              = Column(Integer, primary_key=True, autoincrement=True)
    rule_id         = Column(Integer, ForeignKey('global_ignore_rules.id'), nullable=False, unique=True)
    enabled         = Column(Boolean, nullable=False, default=False)
    last_changed_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    # Relaciones
    rule            = relationship("GlobalIgnoreRules", back_populates="user_override")


# 11. TAREAS PETICIONES AL SERVIDOR
class ServerTasks(Base):
    __tablename__   = 'server_tasks'
    id              = Column(Integer, primary_key=True, autoincrement=True)
    task_id         = Column(String, nullable=False, unique=True)
    state           = Column(String, nullable=False, default='QUEUE')
    created_at      = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    __table_args__  = (CheckConstraint(
            "state IN ('QUEUE', 'PROCESSING', 'COMPLETE', 'ERROR')",
            name='check_valid_state'
    ),)

    def to_dict(self):
        return {
            "id": self.id,
            "task_id": self.task_id,
            "state": self.state,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }


# 12. COLA DE SINCRONIZACIÓN (Offline mode para el Oráculo)
#class OracleQueue(Base):
#    __tablename__ = 'oracle_queue'
