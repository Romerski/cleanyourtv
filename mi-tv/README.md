# TCL 75C89K: limpieza con CleanYourTV (19-11-2026)

TV: TCL 75C89K, "Smart TV Pro", G08 / G08_4K_GB, Google TV 14, firmware `UTT2.250416.001 AU02`.
IP en tu red: `192.168.100.150` (Ethernet). Base: `examples/tcl-c89b-google-tv` del repo
[Gathin23/cleanyourtv](https://github.com/Gathin23/cleanyourtv), mismo producto y firmware.

## Este repo

Es un fork de CleanYourTV con mi configuración: esta carpeta `mi-tv/` y los cambios del launcher ya hechos en su
código (`launcher/`). Para traer las novedades del proyecto original: botón **Sync fork** en GitHub, o
`git pull https://github.com/Gathin23/cleanyourtv main`.

Desde cualquier ordenador Windows (Python 3, y JDK 17 + Android SDK 34 solo si vas a recompilar el launcher):

```powershell
git clone https://github.com/Romerski/cleanyourtv; cd cleanyourtv
python -m venv tools\venv; tools\venv\Scripts\python.exe -m pip install -r tools\requirements.txt
$env:TV_HOST = '192.168.100.150'        # la IP de la TV; en la TV: Opciones de desarrollador > Depuración USB
powershell -ExecutionPolicy Bypass -File tools\disable.ps1 mi-tv\debloat.txt
powershell -ExecutionPolicy Bypass -File launcher\build-and-install.ps1 -StockLauncher none -HomeKeyService
tools\venv\Scripts\python.exe -I tools\b64push.py mi-tv\rog-ally\rog-ally.apk /data/local/tmp/rogally.apk
tools\venv\Scripts\python.exe -I tools\tv.py 'pm install -r /data/local/tmp/rogally.apk; rm /data/local/tmp/rogally.apk'
powershell -ExecutionPolicy Bypass -File tools\theme.ps1 mi-tv\mi-tema
```

En una TV nueva el orden es el de arriba, pero las dos últimas líneas de `debloat.txt` (setupwraith y launcherx) solo se
desactivan cuando el launcher nuevo ya está instalado: ejecuta `disable.ps1` otra vez después de `build-and-install.ps1`.
Con Claude Code basta con abrir el repo y pedirle «aplica la configuración de `mi-tv` a esta TV».

## Qué se hizo

| Paso | Detalle |
|---|---|
| Backup | Lista de paquetes, `getprop`, settings global/secure/system, Home original, tamaño/densidad de pantalla. En `backup/`, **limpio**: número de serie, Bluetooth, `android_id`, IPs y demás identificadores tachados (`backup/README.md`) |
| Debloat | 30 paquetes desactivados con `pm disable-user --user 0` (nada desinstalado), en 4 lotes: ver `debloat.txt` |
| Salvapantallas | Ambient de Google (`dreamx`, con promos) cambiado a `com.android.dreams.basic/.Colors` |
| Launcher | CleanYourTV v3.5 (`com.gathin.tvhome`) como Home; dock: TiviMate, Nuvio, SmartTube, S0undTV, Prime Video, ROG Ally |
| Botones | Helper `HomeKeyService`: Netflix → Nuvio, Prime Video → Prime Video, YouTube → SmartTube, TCL Channel → TiviMate, engranaje → panel de ajustes; `volume_pauses_filter` activo |
| DNS | DNS privado `dns.adguard-dns.com` (bloquea anuncios y rastreadores en todo el sistema; no los de YouTube) |

**Projectivy Launcher desinstalado** (19-11-2026): ya no hacía falta, porque Home, el salvapantallas y los botones van
por CleanYourTV. Su configuración se perdió con él; si lo quieres de vuelta, está en Play Store.
**Launcher Manager** (`com.wolf.google.lm`, instalado a mano desde un APK) también desinstalado ese día, por el mismo motivo.
TV Quick Actions sigue instalado, con su accesibilidad apagada.

**Se conservan a propósito:** Alexa (`com.tcl.smartalexa` + `com.tcl.ttvs`), cuenta TCL (`com.tcl.usercenter`),
Chromecast, AirPlay, Miracast, Netflix, Prime Video, Game Bar, YouTube Music, el reproductor USB y la galería.

`com.tcl.ttvs` contiene a la vez el núcleo de Alexa, el actualizador de firmware de TCL **y** Samba TV ACR (la
analítica que reconoce lo que ves). No se puede desactivar solo una parte sin root. Para cortar el ACR, desactívalo
desde el menú de la TV: Ajustes → Privacidad (o Sistema → Privacidad), opciones del tipo
"Servicios de información de visualización", "Smart TV interactivity" o "Samba TV".

## Estilo, salvapantallas y add-ons (19-11-2026)

| Qué | Detalle |
|---|---|
| Tema | `mi-tema/`: el tema `ambient-glass` del repo (8 paisajes alpinos y de desierto que cambian cada 5 min, con su pie de foto; dock de cristal esmerilado, botones solo con icono) con 6 columnas y 6 apps en el dock (TiviMate, Nuvio, SmartTube, S0undTV, Prime Video, ROG Ally), más Live TV y tus botones. `advanced_effects` activo: el icono enfocado se amplía un poco más (1,12× en vez de 1,10×), se eleva con sombra y su imagen hace zoom. Créditos de las fotos (licencia Unsplash) en `mi-tema/CREDITS.md` |
| Tema anterior | `mi-tema-aerial/`: el tema aerial (fotos de la ISS) con los mismos botones; para volver a él, envía esa carpeta con `theme.ps1` |
| Salvapantallas | El reloj del launcher (`com.gathin.tvhome/.ClockDream`), sobre el fondo del tema |
| Mandos de juego | `gamepad_passthrough`: con un mando conectado (Moonlight), el helper deja pasar todos sus botones; los atajos del mando de la TV no funcionan hasta que lo desconectes |
| Add-ons | **Weather** (el tiempo de tu ciudad, de Open-Meteo). Sources se instaló y lo desinstalaste: el menú de entradas del launcher ya da los nombres de los aparatos por CEC («ASUS ROG Ally · HDMI 2»). La primera vez que se instala un add-on, Home pregunta si mostrar su tarjeta; para cambiarlo después: mantén OK sobre Ajustes → Module cards |
| Menú de entradas | El desplegable de arriba a la derecha: HDMI 1–4 (con el aparato conectado por CEC), **AirPlay** y TV en vivo. El botón Entradas del mando lo abre en lugar del panel de TCL |

Quitar el tema: `tools\theme.ps1 -TvHost 192.168.100.150 -Reset`. Desinstalar un add-on: Ajustes → Aplicaciones.
Volver al salvapantallas anterior: `settings put secure screensaver_components com.android.dreams.basic/.Colors`.

## Botones del mando y TV Quick Actions

Los atajos los hace el helper `HomeKeyService` del launcher. TV Quick Actions hacía los mismos atajos a la vez
(cada app se abría dos veces) y su filtro de teclas cortaba el volumen mantenido, así que **se apagó su servicio
de accesibilidad** (la app sigue instalada; si la abres y te pide el permiso de accesibilidad, no se lo des).
Probado con el mando real el 19-11-2026: cada botón abre su app una vez y mantener VOL− baja el volumen de forma
continua.

Keycodes de este mando (leídos del log `InputReader: TIDD`):

| Botón | keycode | scancode | Ahora abre |
|---|---|---|---|
| Netflix | 4062 | 566 | Nuvio (`com.nuvio.app`; antes de una reinstalación era `com.nuvio.tv`) |
| Prime Video | 4099 | 752 | Prime Video |
| YouTube | 190 | 569 | SmartTube |
| TCL Channel | 4020 | | TiviMate |
| TV (debajo de la casita) | 4001 | 365 | TV en directo (TDT); con la TDT delante, la guía; con la guía delante, la cierra |
| Entradas | 178 (`KEYCODE_TV_INPUT`) | 471 | Menú de entradas del launcher (`"178:inputs"`), no el panel de TCL |
| Engranaje | 83 | 561 | Panel de ajustes del launcher |
| Home / Atrás | 3 / 4 | 102 / 158 | (sistema) |
| Canal + / − | 166 / 167 | 402 / 403 | (sistema) |
| Volumen + / − | 24 / 25 | 115 / 114 | (sistema) |

### Cambios propios en el código del launcher (`cambios-launcher.patch`)

Tres cosas no se podían hacer solo con ajustes, así que el launcher instalado lleva un pequeño parche (52 líneas):

1. **Botón TV y guía.** El botón TV lo gestionaba el Home de Google TV; la app de TV de TCL no hace nada con él por sí
   sola. Ahora: `"4001:com.tcl.tv"` abre la TDT y `"front:4001:guide:com.tcl.tv"` abre la guía con la TV delante. El
   parche hace que el helper recuerde también qué pantalla está delante y, si ya es la guía, haga Atrás en vez de
   abrirla otra vez.
2. **AirPlay en el menú de entradas.** El receptor AirPlay de la TV es una entrada de software
   (`com.mediatek.AirplayAPK/.AirPlayTvInputService`), no un puerto, y el menú solo listaba puertos. El parche añade una
   fila «AirPlay» (con su icono, `ic_airplay.xml`) que abre esa entrada en la app de TV de TCL, igual que hace el panel de TCL.
3. **El botón Entradas cierra el menú.** El launcher recuerda si su menú de entradas está abierto; si lo está, el botón
   Entradas hace Atrás en vez de abrirlo otra vez, igual que el botón TV con la guía.

En este fork los tres cambios ya están en el código de `launcher/`, y `cleanyourtv-launcher.apk` los incluye. Con
**Sync fork** git los mantiene al traer novedades; si alguna vez choca con un cambio del original, GitHub te lo dirá
y habrá que resolverlo a mano. `cambios-launcher.patch` es el mismo cambio en un solo fichero, para aplicarlo
(`git apply`) sobre una copia limpia del repo original. Sin estos cambios todo lo demás funciona; solo faltan la fila
de AirPlay y que los botones TV y Entradas cierren lo que abrieron (Atrás lo cierra igual).

### Ficha «ROG Ally» (`rog-ally/`)

Mini-app propia (`io.github.romerski.rogally`, 72 KB, sin permisos) que aparece en el dock con un icono dibujado para
ella (`draw_icon.py`; no es el logo de ROG). No tiene pantalla: al abrirla cambia la TV a la entrada HDMI de la Ally,
en este orden:

1. una entrada con «Ally» en el nombre: el nombre HDMI-CEC del aparato («ASUS ROG Ally») o el que le pongas a su
   puerto en Ajustes > Entradas. La dock no siempre se anuncia por CEC, así que no se puede contar solo con esto;
2. si no, el único puerto HDMI con algo encendido detrás (TCL marca los vacíos como «en espera»), así que sigue al
   cable si lo cambias de puerto mientras la Ally sea el único aparato HDMI;
3. si no, el último puerto donde la encontró y, la primera vez, el HDMI 2.

Probado el 21-11-2026: la ficha abre el HDMI 2 con la imagen de la Ally.

**Cambio automático al despertar la Ally: no es posible tal como está.** Probado el 21-11-2026: al despertarla con su
mando, la dock no manda ningún mensaje HDMI-CEC (el historial CEC de la TV está vacío) y el HDMI 2 sigue en estado
«conectado» también con la Ally en reposo, así que la TV no tiene nada que detectar. Si algún día la Ally o su dock
empiezan a mandar CEC (*One Touch Play*), la TV podría cambiar sola.

Recompilar: `cd mi-tv\rog-ally; .\gradlew.bat assembleRelease` (JDK 17 y SDK 34, como el launcher) e instalar
`app\build\outputs\apk\release\app-release.apk` como en «Este repo». `rog-ally.apk` es esa misma build.

### Tarjeta del tiempo (Weather)

Las tarjetas de add-ons son **fijas**: muestran nombre, un subtítulo y un color, pero no datos en vivo, porque el
launcher no tiene permiso de red y nunca lee nada de internet. Para ver el tiempo hay que abrir la tarjeta. Si lo
quieres a mano, ponla en el dock: mantén OK sobre ella → *Mover*.

### Añadir o cambiar un atajo (sin recompilar)

1. Averigua el keycode del botón: con el repo y su venv, ejecuta lo siguiente y pulsa el botón durante esos 15 s:
   `tools\venv\Scripts\python.exe -I tools\tv.py "logcat -c; sleep 15; logcat -d | grep 'InputReader.*TIDD.*ACTION_DOWN'"`
   (con `$env:TV_HOST = '192.168.100.150'`). El número tras `keyCode=` es el que necesitas.
2. Añádelo a `app_keys` en `mi-tema/config.json`. Formatos:
   - `"4062:com.nuvio.tv"`: un toque abre esa app.
   - `"hold:4062:org.xbmc.kodi"`: mantener pulsado abre otra (el toque sigue igual).
   - Acciones en lugar de app: `mute`, `sleep`, `screensaver`, `settings`, `home`, `back`, `ignore` (anula el botón).
   - `"inputs"` abre el menú de entradas; `"input:<id>"` va directo a un HDMI (ids con `tools\tv.py "dumpsys tv_input"`).
3. Envíalo: `powershell -ExecutionPolicy Bypass -File tools\theme.ps1 -TvHost 192.168.100.150 <ruta a mi-tema>`.
   Sin recompilar; Home se reinicia una vez. `tools\theme.ps1 -TvHost 192.168.100.150 -Reset` lo quita.

`mi-tema/config.json` ya contiene la configuración actual (dock, Live TV y botones), así que solo hay que añadir líneas.
Lista completa de opciones: `themes/README.md` del repo.

## Mantener pulsado el volumen

Con TV Quick Actions apagado, el volumen mantenido funciona normal. Si alguna vez vuelve a ir paso a paso,
`volume_pauses_filter` (activo) lo arregla así: **pulsa una vez y, en los 4 segundos siguientes, mantén pulsado**.

## Deshacerlo todo

Con el repo clonado y su venv (`tools\venv`), desde la raíz del repo:

```powershell
powershell -ExecutionPolicy Bypass -File tools\restore.ps1 -TvHost 192.168.100.150 <ruta a este debloat.txt> -Stock com.google.android.apps.tv.launcherx
```

El registro del estado original está en `%USERPROFILE%\.cleanyourtv\`. Sin repo ni registro, `restore-commands.txt`
contiene los mismos comandos, uno por línea: `tools\tv.py --batch < restore-commands.txt`, o pásalos uno a uno con
cualquier cliente ADB (`adb shell pm enable ...`).

Fuera de esa lista, por separado:

```text
settings put global private_dns_mode opportunistic                                  # quitar AdGuard DNS
settings put secure screensaver_components com.google.android.apps.tv.dreamx/.service.Backdrop   # salvapantallas original
```

Reactivar una sola app sin ordenador: Ajustes → Aplicaciones → Ver todas → (mostrar apps del sistema) → la app → Habilitar.
El launcher de CleanYourTV se queda instalado; desinstálalo en Ajustes → Aplicaciones si ya no lo quieres.

## Cambiar dock, columnas o fondo

- **En la TV:** mantén OK sobre *Ajustes* (arriba a la derecha) → *Reordenar apps*, o mantén OK sobre un icono → *Mover*.
- **Sin recompilar:** edita `mi-tema/config.json` (por ejemplo `"dock_apps"` o `"columns": 5`) y envíalo con
  `tools\theme.ps1 -TvHost 192.168.100.150 <ruta a mi-tema>`. Los temas del repo (fondos, colores) están en `themes/`.
- **Recompilando:** la configuración ya está en `launcher\app\src\main\res\values\config.xml` de este repo; edítalo y
  ejecuta `launcher\build-and-install.ps1 -TvHost 192.168.100.150 -StockLauncher none -HomeKeyService`.

## Tras una actualización de firmware

Puede devolver paquetes y el Home de Google TV. Activa la depuración otra vez y ejecuta
`tools\venv\Scripts\python.exe -I tools\check.py <debloat.txt>` (`--fix` lo vuelve a aplicar).
`cleanyourtv-launcher.apk` es el launcher ya compilado: `SKIP_BUILD=1` con `build-and-install.ps1` lo reinstala sin compilar
(cópialo antes a `launcher\app\build\outputs\apk\release\app-release.apk`).

## Depuración ADB (puerto 5555)

El puerto 5555 va sin cifrar: cualquier dispositivo de tu red al que la TV haya autorizado puede abrir una shell en ella.
Cuando no lo uses: Ajustes → Sistema → Opciones de desarrollador → **Depuración USB** desactivada y
**Revocar autorizaciones de depuración USB**; reinicia y comprueba con
`tools\venv\Scripts\python.exe -I tools\adb-closed.py 192.168.100.150` (debe decir que está cerrado).
El launcher y sus botones siguen funcionando sin depuración; para cambiar atajos o tras una actualización vuelve a activarla.

## Herramientas instaladas en el PC donde se hizo

- JDK Temurin 17: `%LOCALAPPDATA%\cleanyourtv-build\jdk17`
- Android SDK (cmdline-tools 23, platform 34, build-tools 34.0.0): `%LOCALAPPDATA%\Android\Sdk`

Ninguna se añadió al PATH. Si no vas a recompilar, puedes borrar las dos carpetas.
