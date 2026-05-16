Lejos de ser un producto cerrado, la arquitectura modular del proyecto se ha diseñado específicamente para soportar iteraciones y mejoras continuas orientadas a consolidarse como una herramienta nativa indispensable en distribuciones Linux.

**Backups Unificados**
Implementación del objetivo extra para generar "fotos fijas" del sistema en formato tar.gz. Esto facilitará drásticamente la migración rápida del usuario al cambiar entre diferentes distribuciones (ej. de Arch a Debian) o ante recuperaciones de desastres.

**IA Privada (Modelos Locales)**
Aunque actualmente el servidor consume la API de Gemini, una vía de desarrollo futuro es la integración con ecosistemas de ejecución local como Ollama. Esto permitiría a los usuarios clasificar sus configuraciones garantizando un aislamiento total de los datos fuera de la red pública.

**Automatización Silenciosa**
Desarrollo definitivo del modo Headless (CLI) para integrar la herramienta directamente con demonios del sistema como cron o systemd timers, permitiendo que el versionado y los escaneos ocurran de manera invisible en segundo plano.

## Soporte Multi-usuario y Sincronización Cloud

Explorar la posibilidad de sincronizar repositorios Git Bare privados entre múltiples máquinas de un mismo usuario de forma cifrada y automática.



---