# Backup de la TV antes de la limpieza (19-11-2026)

Estado de la TCL 75C89K antes de tocar nada: paquetes instalados (`packages-*.txt`, ninguno desactivado de fábrica),
propiedades del sistema (`getprop.txt`), ajustes (`settings-global/secure/system.txt`), el Home original
(`home-activity.txt`: `com.google.android.apps.tv.launcherx`) y la pantalla (`display.txt`).

**Versión limpia para un repo público.** Los valores que identifican la TV o su red se han sustituido por
`<redacted>`: número de serie, dirección y nombre Bluetooth, `android_id`, nombre del dispositivo, IDs de entrada de
TCL, IPs, MACs, emails y cadenas largas con aspecto de identificador. Por precaución también se taparon algunos
ajustes inofensivos con palabras como `bluetooth`, `location` o `account` en el nombre. El resto está tal cual.

Para deshacer la limpieza no hace falta este backup: usa `../restore-commands.txt` o `tools\restore.ps1` (ver
`../README.md`). Sirve como referencia de cómo venía la TV de fábrica.
