# KG TRACKER - COMPLETE TECHNICAL AUDIT
Technical snapshot generated automatically. This is not a release verdict.
This script does not modify project source code.

Project root: F:\KURIGAMESDEV\KG TRACKER
Audit date: 2026-09-15 19:52:09


## 1. Git status and history

### Git status

```text
## main
?? _audit/
?? scripts/AUDIT_KG_TRACKER.ps1
?? ui/main_window.py.anim_fix_bak
?? ui/main_window.py.bak_signal
?? ui/main_window_games.py.anim_fix_bak
?? ui/main_window_games.py.bak2
?? ui/main_window_navigation.py.anim_fix_bak
?? ui/main_window_navigation.py.bak2
```

### Recent commits

```text
5a14bcc (HEAD -> main) feat(release): refactorizacion de seguridad, rutas, validadores y suite de tests para v0.2.35
aba9ab7 (origin/main, origin/HEAD) v0.2.35: incorporar soporte bilingue en README.md y README_ES.md con nota del autor
a8a6efd v0.2.34: proteger reloj maestro frente a reciclado de tarjetas, eliminar artefactos de node y crear CHANGELOG.md
60382fa v0.2.33: aislar senales de trabajadores de busqueda en segundo plano y normalizar codificacion UTF-8 en config.py
4df5867 v0.2.32: redise├▒ar README.md con formato profesional sin emojis y codificacion UTF-8 estricta
302c160 v0.2.31: ampliar cobertura de pruebas unitarias para resiliencia de i18n, enriquecedor de steam y traductor
4647454 v0.2.30: estandarizar persistencia atomica de configuracion y caches json en storage y sincronizar README con version v0.2.29
e418f96 v0.2.29: ignorar datos runtime del usuario en gitignore y eliminar scripts obsoletos de studio
35cccb1 v0.2.28: aislar sesiones http concurrentes por scraper y escapar caracteres reservados de powershell en notificaciones push
e6dfaf5 v0.2.27: estandarizar persistencia atomica de caches json en storage y sincronizar README con version v0.2.26 y licencia no comercial
da4ea24 v0.2.26: eliminar desplazamiento vertical de tarjetas restaurando apertura directa sincronizada con el desplegable
e0b127f v0.2.25: corregir comilla doble sin escapar en clase de caracteres regex en normalizacion de titulos
```

### Tags

```text
v0.2.0
v0.1.34-stable
v0.1.6-stable
v0.1.5-stable
v0.1.23
v0.1.21
v0.1.20
v0.1.19
v0.1.18
v0.1.4-no-stable
v0.1.3
v0.1.2
v0.1.1
stable
v0.1-stable
v5.0
```

### Recent diff statistics

```text
[No output]
```


## 2. Project structure

### Top-level files and folders

```text

Mode   Length LastWriteTime       Name             
----   ------ -------------       ----             
d-----        15/09/2026 19:52:10 .git             
d-----        09/09/2026 0:56:09  .venv            
d-----        13/09/2026 22:51:31 .vscode          
d-----        13/09/2026 2:25:36  assets           
d-----        14/09/2026 21:45:33 cache            
d-----        15/09/2026 1:19:06  core             
d-----        15/09/2026 19:43:21 data             
d-----        13/09/2026 2:24:48  docs             
d-----        15/09/2026 0:10:57  logs             
d-----        13/09/2026 1:18:12  node_modules     
d-----        15/09/2026 2:40:44  scripts          
d-----        15/09/2026 1:28:03  tests            
d-----        15/09/2026 2:52:29  ui               
d-----        15/09/2026 19:52:09 _audit           
d-----        15/09/2026 1:24:07  __pycache__      
-a---- 68     01/09/2026 1:11:24  .gitattributes   
-a---- 571    14/09/2026 23:42:35 .gitignore       
-a---- 3087   15/09/2026 1:20:14  build.py         
-a---- 8336   14/09/2026 15:58:50 cls              
-a---- 3967   15/09/2026 0:40:04  config.py        
-a---- 1366   15/09/2026 1:20:08  KGameTracker.spec
-a---- 1419   09/09/2026 3:23:14  LICENSE          
-a---- 6066   14/09/2026 1:56:32  logger.py        
-a---- 6192   14/09/2026 1:56:32  main.py          
-a---- 1445   15/09/2026 1:20:19  PRIVACY.md       
-a---- 3842   15/09/2026 0:49:48  README.md        
-a---- 4218   15/09/2026 0:49:48  README_ES.md     
-a---- 488    12/09/2026 23:58:49 requirements.txt 
-a---- 896    15/09/2026 1:20:20  SECURITY.md
```

### Python files

```text
.venv\Lib\site-packages\certifi\__init__.py
.venv\Lib\site-packages\certifi\__main__.py
.venv\Lib\site-packages\certifi\core.py
.venv\Lib\site-packages\certifi\tests\__init__.py
.venv\Lib\site-packages\certifi\tests\test_certify.py
.venv\Lib\site-packages\charset_normalizer\__init__.py
.venv\Lib\site-packages\charset_normalizer\__main__.py
.venv\Lib\site-packages\charset_normalizer\api.py
.venv\Lib\site-packages\charset_normalizer\cd.py
.venv\Lib\site-packages\charset_normalizer\cli\__init__.py
.venv\Lib\site-packages\charset_normalizer\cli\__main__.py
.venv\Lib\site-packages\charset_normalizer\constant.py
.venv\Lib\site-packages\charset_normalizer\legacy.py
.venv\Lib\site-packages\charset_normalizer\md.py
.venv\Lib\site-packages\charset_normalizer\models.py
.venv\Lib\site-packages\charset_normalizer\utils.py
.venv\Lib\site-packages\charset_normalizer\version.py
.venv\Lib\site-packages\idna\__init__.py
.venv\Lib\site-packages\idna\__main__.py
.venv\Lib\site-packages\idna\cli.py
.venv\Lib\site-packages\idna\codec.py
.venv\Lib\site-packages\idna\compat.py
.venv\Lib\site-packages\idna\core.py
.venv\Lib\site-packages\idna\idnadata.py
.venv\Lib\site-packages\idna\intranges.py
.venv\Lib\site-packages\idna\package_data.py
.venv\Lib\site-packages\idna\uts46data.py
.venv\Lib\site-packages\numpy\__config__.py
.venv\Lib\site-packages\numpy\__init__.py
.venv\Lib\site-packages\numpy\_array_api_info.py
.venv\Lib\site-packages\numpy\_configtool.py
.venv\Lib\site-packages\numpy\_core\__init__.py
.venv\Lib\site-packages\numpy\_core\_add_newdocs.py
.venv\Lib\site-packages\numpy\_core\_add_newdocs_scalars.py
.venv\Lib\site-packages\numpy\_core\_asarray.py
.venv\Lib\site-packages\numpy\_core\_dtype.py
.venv\Lib\site-packages\numpy\_core\_dtype_ctypes.py
.venv\Lib\site-packages\numpy\_core\_exceptions.py
.venv\Lib\site-packages\numpy\_core\_internal.py
.venv\Lib\site-packages\numpy\_core\_methods.py
.venv\Lib\site-packages\numpy\_core\_string_helpers.py
.venv\Lib\site-packages\numpy\_core\_type_aliases.py
.venv\Lib\site-packages\numpy\_core\_ufunc_config.py
.venv\Lib\site-packages\numpy\_core\arrayprint.py
.venv\Lib\site-packages\numpy\_core\cversions.py
.venv\Lib\site-packages\numpy\_core\defchararray.py
.venv\Lib\site-packages\numpy\_core\einsumfunc.py
.venv\Lib\site-packages\numpy\_core\fromnumeric.py
.venv\Lib\site-packages\numpy\_core\function_base.py
.venv\Lib\site-packages\numpy\_core\getlimits.py
.venv\Lib\site-packages\numpy\_core\memmap.py
.venv\Lib\site-packages\numpy\_core\multiarray.py
.venv\Lib\site-packages\numpy\_core\numeric.py
.venv\Lib\site-packages\numpy\_core\numerictypes.py
.venv\Lib\site-packages\numpy\_core\overrides.py
.venv\Lib\site-packages\numpy\_core\printoptions.py
.venv\Lib\site-packages\numpy\_core\records.py
.venv\Lib\site-packages\numpy\_core\shape_base.py
.venv\Lib\site-packages\numpy\_core\strings.py
.venv\Lib\site-packages\numpy\_core\tests\_locales.py
.venv\Lib\site-packages\numpy\_core\tests\_natype.py
.venv\Lib\site-packages\numpy\_core\tests\examples\cython\setup.py
.venv\Lib\site-packages\numpy\_core\tests\examples\limited_api\setup.py
.venv\Lib\site-packages\numpy\_core\tests\test__exceptions.py
.venv\Lib\site-packages\numpy\_core\tests\test_abc.py
.venv\Lib\site-packages\numpy\_core\tests\test_api.py
.venv\Lib\site-packages\numpy\_core\tests\test_argparse.py
.venv\Lib\site-packages\numpy\_core\tests\test_array_api_info.py
.venv\Lib\site-packages\numpy\_core\tests\test_array_coercion.py
.venv\Lib\site-packages\numpy\_core\tests\test_array_interface.py
.venv\Lib\site-packages\numpy\_core\tests\test_arraymethod.py
.venv\Lib\site-packages\numpy\_core\tests\test_arrayobject.py
.venv\Lib\site-packages\numpy\_core\tests\test_arrayprint.py
.venv\Lib\site-packages\numpy\_core\tests\test_casting_floatingpoint_errors.py
.venv\Lib\site-packages\numpy\_core\tests\test_casting_unittests.py
.venv\Lib\site-packages\numpy\_core\tests\test_conversion_utils.py
.venv\Lib\site-packages\numpy\_core\tests\test_cpu_dispatcher.py
.venv\Lib\site-packages\numpy\_core\tests\test_cpu_features.py
.venv\Lib\site-packages\numpy\_core\tests\test_custom_dtypes.py
.venv\Lib\site-packages\numpy\_core\tests\test_cython.py
.venv\Lib\site-packages\numpy\_core\tests\test_datetime.py
.venv\Lib\site-packages\numpy\_core\tests\test_defchararray.py
.venv\Lib\site-packages\numpy\_core\tests\test_deprecations.py
.venv\Lib\site-packages\numpy\_core\tests\test_dlpack.py
.venv\Lib\site-packages\numpy\_core\tests\test_dtype.py
.venv\Lib\site-packages\numpy\_core\tests\test_einsum.py
.venv\Lib\site-packages\numpy\_core\tests\test_errstate.py
.venv\Lib\site-packages\numpy\_core\tests\test_extint128.py
.venv\Lib\site-packages\numpy\_core\tests\test_finfo.py
.venv\Lib\site-packages\numpy\_core\tests\test_function_base.py
.venv\Lib\site-packages\numpy\_core\tests\test_getlimits.py
.venv\Lib\site-packages\numpy\_core\tests\test_half.py
.venv\Lib\site-packages\numpy\_core\tests\test_hashtable.py
.venv\Lib\site-packages\numpy\_core\tests\test_indexerrors.py
.venv\Lib\site-packages\numpy\_core\tests\test_indexing.py
.venv\Lib\site-packages\numpy\_core\tests\test_item_selection.py
.venv\Lib\site-packages\numpy\_core\tests\test_limited_api.py
.venv\Lib\site-packages\numpy\_core\tests\test_longdouble.py
.venv\Lib\site-packages\numpy\_core\tests\test_mem_overlap.py
.venv\Lib\site-packages\numpy\_core\tests\test_mem_policy.py
.venv\Lib\site-packages\numpy\_core\tests\test_memmap.py
.venv\Lib\site-packages\numpy\_core\tests\test_multiarray.py
.venv\Lib\site-packages\numpy\_core\tests\test_multiprocessing.py
.venv\Lib\site-packages\numpy\_core\tests\test_multithreading.py
.venv\Lib\site-packages\numpy\_core\tests\test_nditer.py
.venv\Lib\site-packages\numpy\_core\tests\test_nep50_promotions.py
.venv\Lib\site-packages\numpy\_core\tests\test_numeric.py
.venv\Lib\site-packages\numpy\_core\tests\test_numerictypes.py
.venv\Lib\site-packages\numpy\_core\tests\test_overrides.py
.venv\Lib\site-packages\numpy\_core\tests\test_print.py
.venv\Lib\site-packages\numpy\_core\tests\test_protocols.py
.venv\Lib\site-packages\numpy\_core\tests\test_records.py
.venv\Lib\site-packages\numpy\_core\tests\test_regression.py
.venv\Lib\site-packages\numpy\_core\tests\test_scalar_ctors.py
.venv\Lib\site-packages\numpy\_core\tests\test_scalar_methods.py
.venv\Lib\site-packages\numpy\_core\tests\test_scalarbuffer.py
.venv\Lib\site-packages\numpy\_core\tests\test_scalarinherit.py
.venv\Lib\site-packages\numpy\_core\tests\test_scalarmath.py
.venv\Lib\site-packages\numpy\_core\tests\test_scalarprint.py
.venv\Lib\site-packages\numpy\_core\tests\test_shape_base.py
.venv\Lib\site-packages\numpy\_core\tests\test_simd.py
.venv\Lib\site-packages\numpy\_core\tests\test_simd_module.py
.venv\Lib\site-packages\numpy\_core\tests\test_stringdtype.py
.venv\Lib\site-packages\numpy\_core\tests\test_strings.py
.venv\Lib\site-packages\numpy\_core\tests\test_ufunc.py
.venv\Lib\site-packages\numpy\_core\tests\test_umath.py
.venv\Lib\site-packages\numpy\_core\tests\test_umath_accuracy.py
.venv\Lib\site-packages\numpy\_core\tests\test_umath_complex.py
.venv\Lib\site-packages\numpy\_core\tests\test_unicode.py
.venv\Lib\site-packages\numpy\_core\umath.py
.venv\Lib\site-packages\numpy\_distributor_init.py
.venv\Lib\site-packages\numpy\_expired_attrs_2_0.py
.venv\Lib\site-packages\numpy\_globals.py
.venv\Lib\site-packages\numpy\_pyinstaller\__init__.py
.venv\Lib\site-packages\numpy\_pyinstaller\hook-numpy.py
.venv\Lib\site-packages\numpy\_pyinstaller\tests\__init__.py
.venv\Lib\site-packages\numpy\_pyinstaller\tests\pyinstaller-smoke.py
.venv\Lib\site-packages\numpy\_pyinstaller\tests\test_pyinstaller.py
.venv\Lib\site-packages\numpy\_pytesttester.py
.venv\Lib\site-packages\numpy\_typing\__init__.py
.venv\Lib\site-packages\numpy\_typing\_add_docstring.py
.venv\Lib\site-packages\numpy\_typing\_array_like.py
.venv\Lib\site-packages\numpy\_typing\_char_codes.py
.venv\Lib\site-packages\numpy\_typing\_dtype_like.py
.venv\Lib\site-packages\numpy\_typing\_extended_precision.py
.venv\Lib\site-packages\numpy\_typing\_nbit.py
.venv\Lib\site-packages\numpy\_typing\_nbit_base.py
.venv\Lib\site-packages\numpy\_typing\_nested_sequence.py
.venv\Lib\site-packages\numpy\_typing\_scalars.py
.venv\Lib\site-packages\numpy\_typing\_shape.py
.venv\Lib\site-packages\numpy\_typing\_ufunc.py
.venv\Lib\site-packages\numpy\_utils\__init__.py
.venv\Lib\site-packages\numpy\_utils\_conversions.py
.venv\Lib\site-packages\numpy\_utils\_inspect.py
.venv\Lib\site-packages\numpy\_utils\_pep440.py
.venv\Lib\site-packages\numpy\char\__init__.py
.venv\Lib\site-packages\numpy\conftest.py
.venv\Lib\site-packages\numpy\core\__init__.py
.venv\Lib\site-packages\numpy\core\_dtype.py
.venv\Lib\site-packages\numpy\core\_dtype_ctypes.py
.venv\Lib\site-packages\numpy\core\_internal.py
.venv\Lib\site-packages\numpy\core\_multiarray_umath.py
.venv\Lib\site-packages\numpy\core\_utils.py
.venv\Lib\site-packages\numpy\core\arrayprint.py
.venv\Lib\site-packages\numpy\core\defchararray.py
.venv\Lib\site-packages\numpy\core\einsumfunc.py
.venv\Lib\site-packages\numpy\core\fromnumeric.py
.venv\Lib\site-packages\numpy\core\function_base.py
.venv\Lib\site-packages\numpy\core\getlimits.py
.venv\Lib\site-packages\numpy\core\multiarray.py
.venv\Lib\site-packages\numpy\core\numeric.py
.venv\Lib\site-packages\numpy\core\numerictypes.py
.venv\Lib\site-packages\numpy\core\overrides.py
.venv\Lib\site-packages\numpy\core\records.py
.venv\Lib\site-packages\numpy\core\shape_base.py
.venv\Lib\site-packages\numpy\core\umath.py
.venv\Lib\site-packages\numpy\ctypeslib\__init__.py
.venv\Lib\site-packages\numpy\ctypeslib\_ctypeslib.py
.venv\Lib\site-packages\numpy\doc\ufuncs.py
.venv\Lib\site-packages\numpy\dtypes.py
.venv\Lib\site-packages\numpy\exceptions.py
.venv\Lib\site-packages\numpy\f2py\__init__.py
.venv\Lib\site-packages\numpy\f2py\__main__.py
.venv\Lib\site-packages\numpy\f2py\__version__.py
.venv\Lib\site-packages\numpy\f2py\_backends\__init__.py
.venv\Lib\site-packages\numpy\f2py\_backends\_backend.py
.venv\Lib\site-packages\numpy\f2py\_backends\_meson.py
.venv\Lib\site-packages\numpy\f2py\_isocbind.py
.venv\Lib\site-packages\numpy\f2py\_src_pyf.py
.venv\Lib\site-packages\numpy\f2py\auxfuncs.py
.venv\Lib\site-packages\numpy\f2py\capi_maps.py
.venv\Lib\site-packages\numpy\f2py\cb_rules.py
.venv\Lib\site-packages\numpy\f2py\cfuncs.py
.venv\Lib\site-packages\numpy\f2py\common_rules.py
.venv\Lib\site-packages\numpy\f2py\crackfortran.py
.venv\Lib\site-packages\numpy\f2py\diagnose.py
.venv\Lib\site-packages\numpy\f2py\f2py2e.py
.venv\Lib\site-packages\numpy\f2py\f90mod_rules.py
.venv\Lib\site-packages\numpy\f2py\func2subr.py
.venv\Lib\site-packages\numpy\f2py\rules.py
.venv\Lib\site-packages\numpy\f2py\symbolic.py
.venv\Lib\site-packages\numpy\f2py\tests\__init__.py
.venv\Lib\site-packages\numpy\f2py\tests\test_abstract_interface.py
.venv\Lib\site-packages\numpy\f2py\tests\test_array_from_pyobj.py
.venv\Lib\site-packages\numpy\f2py\tests\test_assumed_shape.py
.venv\Lib\site-packages\numpy\f2py\tests\test_block_docstring.py
.venv\Lib\site-packages\numpy\f2py\tests\test_callback.py
.venv\Lib\site-packages\numpy\f2py\tests\test_capi_maps.py
.venv\Lib\site-packages\numpy\f2py\tests\test_character.py
.venv\Lib\site-packages\numpy\f2py\tests\test_common.py
.venv\Lib\site-packages\numpy\f2py\tests\test_crackfortran.py
.venv\Lib\site-packages\numpy\f2py\tests\test_data.py
.venv\Lib\site-packages\numpy\f2py\tests\test_docs.py
.venv\Lib\site-packages\numpy\f2py\tests\test_f2cmap.py
.venv\Lib\site-packages\numpy\f2py\tests\test_f2py2e.py
.venv\Lib\site-packages\numpy\f2py\tests\test_inplace.py
.venv\Lib\site-packages\numpy\f2py\tests\test_isoc.py
.venv\Lib\site-packages\numpy\f2py\tests\test_kind.py
.venv\Lib\site-packages\numpy\f2py\tests\test_mixed.py
.venv\Lib\site-packages\numpy\f2py\tests\test_modules.py
.venv\Lib\site-packages\numpy\f2py\tests\test_parameter.py
.venv\Lib\site-packages\numpy\f2py\tests\test_pyf_src.py
.venv\Lib\site-packages\numpy\f2py\tests\test_quoted_character.py
.venv\Lib\site-packages\numpy\f2py\tests\test_regression.py
.venv\Lib\site-packages\numpy\f2py\tests\test_return_character.py
.venv\Lib\site-packages\numpy\f2py\tests\test_return_complex.py
.venv\Lib\site-packages\numpy\f2py\tests\test_return_integer.py
.venv\Lib\site-packages\numpy\f2py\tests\test_return_logical.py
.venv\Lib\site-packages\numpy\f2py\tests\test_return_real.py
.venv\Lib\site-packages\numpy\f2py\tests\test_routines.py
.venv\Lib\site-packages\numpy\f2py\tests\test_semicolon_split.py
.venv\Lib\site-packages\numpy\f2py\tests\test_size.py
.venv\Lib\site-packages\numpy\f2py\tests\test_string.py
.venv\Lib\site-packages\numpy\f2py\tests\test_symbolic.py
.venv\Lib\site-packages\numpy\f2py\tests\test_value_attrspec.py
.venv\Lib\site-packages\numpy\f2py\tests\util.py
.venv\Lib\site-packages\numpy\f2py\use_rules.py
.venv\Lib\site-packages\numpy\fft\__init__.py
.venv\Lib\site-packages\numpy\fft\_helper.py
.venv\Lib\site-packages\numpy\fft\_pocketfft.py
.venv\Lib\site-packages\numpy\fft\tests\__init__.py
.venv\Lib\site-packages\numpy\fft\tests\test_helper.py
.venv\Lib\site-packages\numpy\fft\tests\test_pocketfft.py
.venv\Lib\site-packages\numpy\lib\__init__.py
.venv\Lib\site-packages\numpy\lib\_array_utils_impl.py
.venv\Lib\site-packages\numpy\lib\_arraypad_impl.py
.venv\Lib\site-packages\numpy\lib\_arraysetops_impl.py
.venv\Lib\site-packages\numpy\lib\_arrayterator_impl.py
.venv\Lib\site-packages\numpy\lib\_datasource.py
.venv\Lib\site-packages\numpy\lib\_format_impl.py
.venv\Lib\site-packages\numpy\lib\_function_base_impl.py
.venv\Lib\site-packages\numpy\lib\_histograms_impl.py
.venv\Lib\site-packages\numpy\lib\_index_tricks_impl.py
.venv\Lib\site-packages\numpy\lib\_iotools.py
.venv\Lib\site-packages\numpy\lib\_nanfunctions_impl.py
.venv\Lib\site-packages\numpy\lib\_npyio_impl.py
.venv\Lib\site-packages\numpy\lib\_polynomial_impl.py
.venv\Lib\site-packages\numpy\lib\_scimath_impl.py
.venv\Lib\site-packages\numpy\lib\_shape_base_impl.py
.venv\Lib\site-packages\numpy\lib\_stride_tricks_impl.py
.venv\Lib\site-packages\numpy\lib\_twodim_base_impl.py
.venv\Lib\site-packages\numpy\lib\_type_check_impl.py
.venv\Lib\site-packages\numpy\lib\_ufunclike_impl.py
.venv\Lib\site-packages\numpy\lib\_user_array_impl.py
.venv\Lib\site-packages\numpy\lib\_utils_impl.py
.venv\Lib\site-packages\numpy\lib\_version.py
.venv\Lib\site-packages\numpy\lib\array_utils.py
.venv\Lib\site-packages\numpy\lib\format.py
.venv\Lib\site-packages\numpy\lib\introspect.py
.venv\Lib\site-packages\numpy\lib\mixins.py
.venv\Lib\site-packages\numpy\lib\npyio.py
.venv\Lib\site-packages\numpy\lib\recfunctions.py
.venv\Lib\site-packages\numpy\lib\scimath.py
.venv\Lib\site-packages\numpy\lib\stride_tricks.py
.venv\Lib\site-packages\numpy\lib\tests\__init__.py
.venv\Lib\site-packages\numpy\lib\tests\test__datasource.py
.venv\Lib\site-packages\numpy\lib\tests\test__iotools.py
.venv\Lib\site-packages\numpy\lib\tests\test__version.py
.venv\Lib\site-packages\numpy\lib\tests\test_array_utils.py
.venv\Lib\site-packages\numpy\lib\tests\test_arraypad.py
.venv\Lib\site-packages\numpy\lib\tests\test_arraysetops.py
.venv\Lib\site-packages\numpy\lib\tests\test_arrayterator.py
.venv\Lib\site-packages\numpy\lib\tests\test_format.py
.venv\Lib\site-packages\numpy\lib\tests\test_function_base.py
.venv\Lib\site-packages\numpy\lib\tests\test_histograms.py
.venv\Lib\site-packages\numpy\lib\tests\test_index_tricks.py
.venv\Lib\site-packages\numpy\lib\tests\test_io.py
.venv\Lib\site-packages\numpy\lib\tests\test_loadtxt.py
.venv\Lib\site-packages\numpy\lib\tests\test_mixins.py
.venv\Lib\site-packages\numpy\lib\tests\test_nanfunctions.py
.venv\Lib\site-packages\numpy\lib\tests\test_packbits.py
.venv\Lib\site-packages\numpy\lib\tests\test_polynomial.py
.venv\Lib\site-packages\numpy\lib\tests\test_recfunctions.py
.venv\Lib\site-packages\numpy\lib\tests\test_regression.py
.venv\Lib\site-packages\numpy\lib\tests\test_shape_base.py
.venv\Lib\site-packages\numpy\lib\tests\test_stride_tricks.py
.venv\Lib\site-packages\numpy\lib\tests\test_twodim_base.py
.venv\Lib\site-packages\numpy\lib\tests\test_type_check.py
.venv\Lib\site-packages\numpy\lib\tests\test_ufunclike.py
.venv\Lib\site-packages\numpy\lib\tests\test_utils.py
.venv\Lib\site-packages\numpy\lib\user_array.py
.venv\Lib\site-packages\numpy\linalg\__init__.py
.venv\Lib\site-packages\numpy\linalg\_linalg.py
.venv\Lib\site-packages\numpy\linalg\tests\__init__.py
.venv\Lib\site-packages\numpy\linalg\tests\test_deprecations.py
.venv\Lib\site-packages\numpy\linalg\tests\test_linalg.py
.venv\Lib\site-packages\numpy\linalg\tests\test_regression.py
.venv\Lib\site-packages\numpy\ma\__init__.py
.venv\Lib\site-packages\numpy\ma\core.py
.venv\Lib\site-packages\numpy\ma\extras.py
.venv\Lib\site-packages\numpy\ma\mrecords.py
.venv\Lib\site-packages\numpy\ma\tests\__init__.py
.venv\Lib\site-packages\numpy\ma\tests\test_arrayobject.py
.venv\Lib\site-packages\numpy\ma\tests\test_core.py
.venv\Lib\site-packages\numpy\ma\tests\test_deprecations.py
.venv\Lib\site-packages\numpy\ma\tests\test_extras.py
.venv\Lib\site-packages\numpy\ma\tests\test_mrecords.py
.venv\Lib\site-packages\numpy\ma\tests\test_old_ma.py
.venv\Lib\site-packages\numpy\ma\tests\test_regression.py
.venv\Lib\site-packages\numpy\ma\tests\test_subclassing.py
.venv\Lib\site-packages\numpy\ma\testutils.py
.venv\Lib\site-packages\numpy\matlib.py
.venv\Lib\site-packages\numpy\matrixlib\__init__.py
.venv\Lib\site-packages\numpy\matrixlib\defmatrix.py
.venv\Lib\site-packages\numpy\matrixlib\tests\__init__.py
.venv\Lib\site-packages\numpy\matrixlib\tests\test_defmatrix.py
.venv\Lib\site-packages\numpy\matrixlib\tests\test_interaction.py
.venv\Lib\site-packages\numpy\matrixlib\tests\test_masked_matrix.py
.venv\Lib\site-packages\numpy\matrixlib\tests\test_matrix_linalg.py
.venv\Lib\site-packages\numpy\matrixlib\tests\test_multiarray.py
.venv\Lib\site-packages\numpy\matrixlib\tests\test_numeric.py
.venv\Lib\site-packages\numpy\matrixlib\tests\test_regression.py
.venv\Lib\site-packages\numpy\polynomial\__init__.py
.venv\Lib\site-packages\numpy\polynomial\_polybase.py
.venv\Lib\site-packages\numpy\polynomial\chebyshev.py
.venv\Lib\site-packages\numpy\polynomial\hermite.py
.venv\Lib\site-packages\numpy\polynomial\hermite_e.py
.venv\Lib\site-packages\numpy\polynomial\laguerre.py
.venv\Lib\site-packages\numpy\polynomial\legendre.py
.venv\Lib\site-packages\numpy\polynomial\polynomial.py
.venv\Lib\site-packages\numpy\polynomial\polyutils.py
.venv\Lib\site-packages\numpy\polynomial\tests\__init__.py
.venv\Lib\site-packages\numpy\polynomial\tests\test_chebyshev.py
.venv\Lib\site-packages\numpy\polynomial\tests\test_classes.py
.venv\Lib\site-packages\numpy\polynomial\tests\test_hermite.py
.venv\Lib\site-packages\numpy\polynomial\tests\test_hermite_e.py
.venv\Lib\site-packages\numpy\polynomial\tests\test_laguerre.py
.venv\Lib\site-packages\numpy\polynomial\tests\test_legendre.py
.venv\Lib\site-packages\numpy\polynomial\tests\test_polynomial.py
.venv\Lib\site-packages\numpy\polynomial\tests\test_polyutils.py
.venv\Lib\site-packages\numpy\polynomial\tests\test_printing.py
.venv\Lib\site-packages\numpy\polynomial\tests\test_symbol.py
.venv\Lib\site-packages\numpy\random\__init__.py
.venv\Lib\site-packages\numpy\random\_examples\cffi\extending.py
.venv\Lib\site-packages\numpy\random\_examples\cffi\parse.py
.venv\Lib\site-packages\numpy\random\_examples\numba\extending.py
.venv\Lib\site-packages\numpy\random\_examples\numba\extending_distributions.py
.venv\Lib\site-packages\numpy\random\_pickle.py
.venv\Lib\site-packages\numpy\random\tests\__init__.py
.venv\Lib\site-packages\numpy\random\tests\data\__init__.py
.venv\Lib\site-packages\numpy\random\tests\test_direct.py
.venv\Lib\site-packages\numpy\random\tests\test_extending.py
.venv\Lib\site-packages\numpy\random\tests\test_generator_mt19937.py
.venv\Lib\site-packages\numpy\random\tests\test_generator_mt19937_regressions.py
.venv\Lib\site-packages\numpy\random\tests\test_random.py
.venv\Lib\site-packages\numpy\random\tests\test_randomstate.py
.venv\Lib\site-packages\numpy\random\tests\test_randomstate_regression.py
.venv\Lib\site-packages\numpy\random\tests\test_regression.py
.venv\Lib\site-packages\numpy\random\tests\test_seed_sequence.py
.venv\Lib\site-packages\numpy\random\tests\test_smoke.py
.venv\Lib\site-packages\numpy\rec\__init__.py
.venv\Lib\site-packages\numpy\strings\__init__.py
.venv\Lib\site-packages\numpy\testing\__init__.py
.venv\Lib\site-packages\numpy\testing\_private\__init__.py
.venv\Lib\site-packages\numpy\testing\_private\extbuild.py
.venv\Lib\site-packages\numpy\testing\_private\utils.py
.venv\Lib\site-packages\numpy\testing\overrides.py
.venv\Lib\site-packages\numpy\testing\print_coercion_tables.py
.venv\Lib\site-packages\numpy\testing\tests\__init__.py
.venv\Lib\site-packages\numpy\testing\tests\test_utils.py
.venv\Lib\site-packages\numpy\tests\__init__.py
.venv\Lib\site-packages\numpy\tests\test__all__.py
.venv\Lib\site-packages\numpy\tests\test_configtool.py
.venv\Lib\site-packages\numpy\tests\test_ctypeslib.py
.venv\Lib\site-packages\numpy\tests\test_lazyloading.py
.venv\Lib\site-packages\numpy\tests\test_matlib.py
.venv\Lib\site-packages\numpy\tests\test_numpy_config.py
.venv\Lib\site-packages\numpy\tests\test_numpy_version.py
.venv\Lib\site-packages\numpy\tests\test_public_api.py
.venv\Lib\site-packages\numpy\tests\test_reloading.py
.venv\Lib\site-packages\numpy\tests\test_scripts.py
.venv\Lib\site-packages\numpy\tests\test_warnings.py
.venv\Lib\site-packages\numpy\typing\__init__.py
.venv\Lib\site-packages\numpy\typing\mypy_plugin.py
.venv\Lib\site-packages\numpy\typing\tests\__init__.py
.venv\Lib\site-packages\numpy\typing\tests\data\pass\arithmetic.py
.venv\Lib\site-packages\numpy\typing\tests\data\pass\array_constructors.py
.venv\Lib\site-packages\numpy\typing\tests\data\pass\array_like.py
.venv\Lib\site-packages\numpy\typing\tests\data\pass\arrayprint.py
.venv\Lib\site-packages\numpy\typing\tests\data\pass\arrayterator.py
.venv\Lib\site-packages\numpy\typing\tests\data\pass\bitwise_ops.py
.venv\Lib\site-packages\numpy\typing\tests\data\pass\comparisons.py
.venv\Lib\site-packages\numpy\typing\tests\data\pass\dtype.py
.venv\Lib\site-packages\numpy\typing\tests\data\pass\einsumfunc.py
.venv\Lib\site-packages\numpy\typing\tests\data\pass\flatiter.py
.venv\Lib\site-packages\numpy\typing\tests\data\pass\fromnumeric.py
.venv\Lib\site-packages\numpy\typing\tests\data\pass\index_tricks.py
.venv\Lib\site-packages\numpy\typing\tests\data\pass\lib_user_array.py
.venv\Lib\site-packages\numpy\typing\tests\data\pass\lib_utils.py
.venv\Lib\site-packages\numpy\typing\tests\data\pass\lib_version.py
.venv\Lib\site-packages\numpy\typing\tests\data\pass\literal.py
.venv\Lib\site-packages\numpy\typing\tests\data\pass\ma.py
.venv\Lib\site-packages\numpy\typing\tests\data\pass\mod.py
.venv\Lib\site-packages\numpy\typing\tests\data\pass\modules.py
.venv\Lib\site-packages\numpy\typing\tests\data\pass\multiarray.py
.venv\Lib\site-packages\numpy\typing\tests\data\pass\ndarray_conversion.py
.venv\Lib\site-packages\numpy\typing\tests\data\pass\ndarray_misc.py
.venv\Lib\site-packages\numpy\typing\tests\data\pass\ndarray_shape_manipulation.py
.venv\Lib\site-packages\numpy\typing\tests\data\pass\nditer.py
.venv\Lib\site-packages\numpy\typing\tests\data\pass\numeric.py
.venv\Lib\site-packages\numpy\typing\tests\data\pass\numerictypes.py
.venv\Lib\site-packages\numpy\typing\tests\data\pass\random.py
.venv\Lib\site-packages\numpy\typing\tests\data\pass\recfunctions.py
.venv\Lib\site-packages\numpy\typing\tests\data\pass\scalars.py
.venv\Lib\site-packages\numpy\typing\tests\data\pass\shape.py
.venv\Lib\site-packages\numpy\typing\tests\data\pass\simple.py
.venv\Lib\site-packages\numpy\typing\tests\data\pass\ufunc_config.py
.venv\Lib\site-packages\numpy\typing\tests\data\pass\ufunclike.py
.venv\Lib\site-packages\numpy\typing\tests\data\pass\ufuncs.py
.venv\Lib\site-packages\numpy\typing\tests\data\pass\warnings_and_errors.py
.venv\Lib\site-packages\numpy\typing\tests\test_isfile.py
.venv\Lib\site-packages\numpy\typing\tests\test_runtime.py
.venv\Lib\site-packages\numpy\typing\tests\test_typing.py
.venv\Lib\site-packages\numpy\version.py
.venv\Lib\site-packages\PIL\__init__.py
.venv\Lib\site-packages\PIL\__main__.py
.venv\Lib\site-packages\PIL\_binary.py
.venv\Lib\site-packages\PIL\_deprecate.py
.venv\Lib\site-packages\PIL\_tkinter_finder.py
.venv\Lib\site-packages\PIL\_typing.py
.venv\Lib\site-packages\PIL\_util.py
.venv\Lib\site-packages\PIL\_version.py
.venv\Lib\site-packages\PIL\AvifImagePlugin.py
.venv\Lib\site-packages\PIL\BdfFontFile.py
.venv\Lib\site-packages\PIL\BlpImagePlugin.py
.venv\Lib\site-packages\PIL\BmpImagePlugin.py
.venv\Lib\site-packages\PIL\BufrStubImagePlugin.py
.venv\Lib\site-packages\PIL\ContainerIO.py
.venv\Lib\site-packages\PIL\CurImagePlugin.py
.venv\Lib\site-packages\PIL\DcxImagePlugin.py
.venv\Lib\site-packages\PIL\DdsImagePlugin.py
.venv\Lib\site-packages\PIL\EpsImagePlugin.py
.venv\Lib\site-packages\PIL\ExifTags.py
.venv\Lib\site-packages\PIL\features.py
.venv\Lib\site-packages\PIL\FitsImagePlugin.py
.venv\Lib\site-packages\PIL\FliImagePlugin.py
.venv\Lib\site-packages\PIL\FontFile.py
.venv\Lib\site-packages\PIL\FpxImagePlugin.py
.venv\Lib\site-packages\PIL\FtexImagePlugin.py
.venv\Lib\site-packages\PIL\GbrImagePlugin.py
.venv\Lib\site-packages\PIL\GdImageFile.py
.venv\Lib\site-packages\PIL\GifImagePlugin.py
.venv\Lib\site-packages\PIL\GimpGradientFile.py
.venv\Lib\site-packages\PIL\GimpPaletteFile.py
.venv\Lib\site-packages\PIL\GribStubImagePlugin.py
.venv\Lib\site-packages\PIL\Hdf5StubImagePlugin.py
.venv\Lib\site-packages\PIL\IcnsImagePlugin.py
.venv\Lib\site-packages\PIL\IcoImagePlugin.py
.venv\Lib\site-packages\PIL\Image.py
.venv\Lib\site-packages\PIL\ImageChops.py
.venv\Lib\site-packages\PIL\ImageCms.py
.venv\Lib\site-packages\PIL\ImageColor.py
.venv\Lib\site-packages\PIL\ImageDraw.py
.venv\Lib\site-packages\PIL\ImageDraw2.py
.venv\Lib\site-packages\PIL\ImageEnhance.py
.venv\Lib\site-packages\PIL\ImageFile.py
.venv\Lib\site-packages\PIL\ImageFilter.py
.venv\Lib\site-packages\PIL\ImageFont.py
.venv\Lib\site-packages\PIL\ImageGrab.py
.venv\Lib\site-packages\PIL\ImageMath.py
.venv\Lib\site-packages\PIL\ImageMode.py
.venv\Lib\site-packages\PIL\ImageMorph.py
.venv\Lib\site-packages\PIL\ImageOps.py
.venv\Lib\site-packages\PIL\ImagePalette.py
.venv\Lib\site-packages\PIL\ImagePath.py
.venv\Lib\site-packages\PIL\ImageQt.py
.venv\Lib\site-packages\PIL\ImageSequence.py
.venv\Lib\site-packages\PIL\ImageShow.py
.venv\Lib\site-packages\PIL\ImageStat.py
.venv\Lib\site-packages\PIL\ImageText.py
.venv\Lib\site-packages\PIL\ImageTk.py
.venv\Lib\site-packages\PIL\ImageTransform.py
.venv\Lib\site-packages\PIL\ImageWin.py
.venv\Lib\site-packages\PIL\ImImagePlugin.py
.venv\Lib\site-packages\PIL\ImtImagePlugin.py
.venv\Lib\site-packages\PIL\IptcImagePlugin.py
.venv\Lib\site-packages\PIL\Jpeg2KImagePlugin.py
.venv\Lib\site-packages\PIL\JpegImagePlugin.py
.venv\Lib\site-packages\PIL\JpegPresets.py
.venv\Lib\site-packages\PIL\McIdasImagePlugin.py
.venv\Lib\site-packages\PIL\MicImagePlugin.py
.venv\Lib\site-packages\PIL\MpegImagePlugin.py
.venv\Lib\site-packages\PIL\MpoImagePlugin.py
.venv\Lib\site-packages\PIL\MspImagePlugin.py
.venv\Lib\site-packages\PIL\PaletteFile.py
.venv\Lib\site-packages\PIL\PalmImagePlugin.py
.venv\Lib\site-packages\PIL\PcdImagePlugin.py
.venv\Lib\site-packages\PIL\PcfFontFile.py
.venv\Lib\site-packages\PIL\PcxImagePlugin.py
.venv\Lib\site-packages\PIL\PdfImagePlugin.py
.venv\Lib\site-packages\PIL\PdfParser.py
.venv\Lib\site-packages\PIL\PixarImagePlugin.py
.venv\Lib\site-packages\PIL\PngImagePlugin.py
.venv\Lib\site-packages\PIL\PpmImagePlugin.py
.venv\Lib\site-packages\PIL\PsdImagePlugin.py
.venv\Lib\site-packages\PIL\PSDraw.py
.venv\Lib\site-packages\PIL\QoiImagePlugin.py
.venv\Lib\site-packages\PIL\report.py
.venv\Lib\site-packages\PIL\SgiImagePlugin.py
.venv\Lib\site-packages\PIL\SpiderImagePlugin.py
.venv\Lib\site-packages\PIL\SunImagePlugin.py
.venv\Lib\site-packages\PIL\TarIO.py
.venv\Lib\site-packages\PIL\TgaImagePlugin.py
.venv\Lib\site-packages\PIL\TiffImagePlugin.py
.venv\Lib\site-packages\PIL\TiffTags.py
.venv\Lib\site-packages\PIL\WalImageFile.py
.venv\Lib\site-packages\PIL\WebPImagePlugin.py
.venv\Lib\site-packages\PIL\WmfImagePlugin.py
.venv\Lib\site-packages\PIL\XbmImagePlugin.py
.venv\Lib\site-packages\PIL\XpmImagePlugin.py
.venv\Lib\site-packages\PIL\XVThumbImagePlugin.py
.venv\Lib\site-packages\pip\__init__.py
.venv\Lib\site-packages\pip\__main__.py
.venv\Lib\site-packages\pip\__pip-runner__.py
.venv\Lib\site-packages\pip\_internal\__init__.py
.venv\Lib\site-packages\pip\_internal\build_env\__init__.py
.venv\Lib\site-packages\pip\_internal\build_env\base.py
.venv\Lib\site-packages\pip\_internal\build_env\installer.py
.venv\Lib\site-packages\pip\_internal\build_env\noop.py
.venv\Lib\site-packages\pip\_internal\build_env\venv.py
.venv\Lib\site-packages\pip\_internal\build_env\virtual.py
.venv\Lib\site-packages\pip\_internal\cache.py
.venv\Lib\site-packages\pip\_internal\cli\__init__.py
.venv\Lib\site-packages\pip\_internal\cli\autocompletion.py
.venv\Lib\site-packages\pip\_internal\cli\base_command.py
.venv\Lib\site-packages\pip\_internal\cli\cmdoptions.py
.venv\Lib\site-packages\pip\_internal\cli\command_context.py
.venv\Lib\site-packages\pip\_internal\cli\index_command.py
.venv\Lib\site-packages\pip\_internal\cli\main.py
.venv\Lib\site-packages\pip\_internal\cli\main_parser.py
.venv\Lib\site-packages\pip\_internal\cli\parser.py
.venv\Lib\site-packages\pip\_internal\cli\progress_bars.py
.venv\Lib\site-packages\pip\_internal\cli\req_command.py
.venv\Lib\site-packages\pip\_internal\cli\spinners.py
.venv\Lib\site-packages\pip\_internal\cli\status_codes.py
.venv\Lib\site-packages\pip\_internal\commands\__init__.py
.venv\Lib\site-packages\pip\_internal\commands\cache.py
.venv\Lib\site-packages\pip\_internal\commands\check.py
.venv\Lib\site-packages\pip\_internal\commands\completion.py
.venv\Lib\site-packages\pip\_internal\commands\configuration.py
.venv\Lib\site-packages\pip\_internal\commands\debug.py
.venv\Lib\site-packages\pip\_internal\commands\download.py
.venv\Lib\site-packages\pip\_internal\commands\freeze.py
.venv\Lib\site-packages\pip\_internal\commands\hash.py
.venv\Lib\site-packages\pip\_internal\commands\help.py
.venv\Lib\site-packages\pip\_internal\commands\index.py
.venv\Lib\site-packages\pip\_internal\commands\inspect.py
.venv\Lib\site-packages\pip\_internal\commands\install.py
.venv\Lib\site-packages\pip\_internal\commands\list.py
.venv\Lib\site-packages\pip\_internal\commands\lock.py
.venv\Lib\site-packages\pip\_internal\commands\search.py
.venv\Lib\site-packages\pip\_internal\commands\show.py
.venv\Lib\site-packages\pip\_internal\commands\uninstall.py
.venv\Lib\site-packages\pip\_internal\commands\wheel.py
.venv\Lib\site-packages\pip\_internal\configuration.py
.venv\Lib\site-packages\pip\_internal\distributions\__init__.py
.venv\Lib\site-packages\pip\_internal\distributions\base.py
.venv\Lib\site-packages\pip\_internal\distributions\installed.py
.venv\Lib\site-packages\pip\_internal\distributions\sdist.py
.venv\Lib\site-packages\pip\_internal\distributions\wheel.py
.venv\Lib\site-packages\pip\_internal\exceptions.py
.venv\Lib\site-packages\pip\_internal\index\__init__.py
.venv\Lib\site-packages\pip\_internal\index\collector.py
.venv\Lib\site-packages\pip\_internal\index\package_finder.py
.venv\Lib\site-packages\pip\_internal\index\sources.py
.venv\Lib\site-packages\pip\_internal\locations\__init__.py
.venv\Lib\site-packages\pip\_internal\locations\_distutils.py
.venv\Lib\site-packages\pip\_internal\locations\_sysconfig.py
.venv\Lib\site-packages\pip\_internal\locations\base.py
.venv\Lib\site-packages\pip\_internal\main.py
.venv\Lib\site-packages\pip\_internal\metadata\__init__.py
.venv\Lib\site-packages\pip\_internal\metadata\_json.py
.venv\Lib\site-packages\pip\_internal\metadata\base.py
.venv\Lib\site-packages\pip\_internal\metadata\importlib\__init__.py
.venv\Lib\site-packages\pip\_internal\metadata\importlib\_compat.py
.venv\Lib\site-packages\pip\_internal\metadata\importlib\_dists.py
.venv\Lib\site-packages\pip\_internal\metadata\importlib\_envs.py
.venv\Lib\site-packages\pip\_internal\metadata\pkg_resources.py
.venv\Lib\site-packages\pip\_internal\models\__init__.py
.venv\Lib\site-packages\pip\_internal\models\candidate.py
.venv\Lib\site-packages\pip\_internal\models\direct_url.py
.venv\Lib\site-packages\pip\_internal\models\format_control.py
.venv\Lib\site-packages\pip\_internal\models\index.py
.venv\Lib\site-packages\pip\_internal\models\installation_report.py
.venv\Lib\site-packages\pip\_internal\models\link.py
.venv\Lib\site-packages\pip\_internal\models\release_control.py
.venv\Lib\site-packages\pip\_internal\models\scheme.py
.venv\Lib\site-packages\pip\_internal\models\search_scope.py
.venv\Lib\site-packages\pip\_internal\models\selection_prefs.py
.venv\Lib\site-packages\pip\_internal\models\target_python.py
.venv\Lib\site-packages\pip\_internal\models\wheel.py
.venv\Lib\site-packages\pip\_internal\network\__init__.py
.venv\Lib\site-packages\pip\_internal\network\auth.py
.venv\Lib\site-packages\pip\_internal\network\cache.py
.venv\Lib\site-packages\pip\_internal\network\download.py
.venv\Lib\site-packages\pip\_internal\network\lazy_wheel.py
.venv\Lib\site-packages\pip\_internal\network\session.py
.venv\Lib\site-packages\pip\_internal\network\utils.py
.venv\Lib\site-packages\pip\_internal\network\xmlrpc.py
.venv\Lib\site-packages\pip\_internal\operations\__init__.py
.venv\Lib\site-packages\pip\_internal\operations\build\__init__.py
.venv\Lib\site-packages\pip\_internal\operations\build\build_tracker.py
.venv\Lib\site-packages\pip\_internal\operations\build\metadata.py
.venv\Lib\site-packages\pip\_internal\operations\build\metadata_editable.py
.venv\Lib\site-packages\pip\_internal\operations\build\wheel.py
.venv\Lib\site-packages\pip\_internal\operations\build\wheel_editable.py
.venv\Lib\site-packages\pip\_internal\operations\check.py
.venv\Lib\site-packages\pip\_internal\operations\freeze.py
.venv\Lib\site-packages\pip\_internal\operations\install\__init__.py
.venv\Lib\site-packages\pip\_internal\operations\install\wheel.py
.venv\Lib\site-packages\pip\_internal\operations\prepare.py
.venv\Lib\site-packages\pip\_internal\pyproject.py
.venv\Lib\site-packages\pip\_internal\req\__init__.py
.venv\Lib\site-packages\pip\_internal\req\constructors.py
.venv\Lib\site-packages\pip\_internal\req\pep723.py
.venv\Lib\site-packages\pip\_internal\req\req_dependency_group.py
.venv\Lib\site-packages\pip\_internal\req\req_file.py
.venv\Lib\site-packages\pip\_internal\req\req_install.py
.venv\Lib\site-packages\pip\_internal\req\req_set.py
.venv\Lib\site-packages\pip\_internal\req\req_uninstall.py
.venv\Lib\site-packages\pip\_internal\resolution\__init__.py
.venv\Lib\site-packages\pip\_internal\resolution\base.py
.venv\Lib\site-packages\pip\_internal\resolution\legacy\__init__.py
.venv\Lib\site-packages\pip\_internal\resolution\legacy\resolver.py
.venv\Lib\site-packages\pip\_internal\resolution\resolvelib\__init__.py
.venv\Lib\site-packages\pip\_internal\resolution\resolvelib\base.py
.venv\Lib\site-packages\pip\_internal\resolution\resolvelib\candidates.py
.venv\Lib\site-packages\pip\_internal\resolution\resolvelib\factory.py
.venv\Lib\site-packages\pip\_internal\resolution\resolvelib\found_candidates.py
.venv\Lib\site-packages\pip\_internal\resolution\resolvelib\provider.py
.venv\Lib\site-packages\pip\_internal\resolution\resolvelib\reporter.py
.venv\Lib\site-packages\pip\_internal\resolution\resolvelib\requirements.py
.venv\Lib\site-packages\pip\_internal\resolution\resolvelib\resolver.py
.venv\Lib\site-packages\pip\_internal\self_outdated_check.py
.venv\Lib\site-packages\pip\_internal\utils\__init__.py
.venv\Lib\site-packages\pip\_internal\utils\_jaraco_text.py
.venv\Lib\site-packages\pip\_internal\utils\_log.py
.venv\Lib\site-packages\pip\_internal\utils\appdirs.py
.venv\Lib\site-packages\pip\_internal\utils\compat.py
.venv\Lib\site-packages\pip\_internal\utils\compatibility_tags.py
.venv\Lib\site-packages\pip\_internal\utils\datetime.py
.venv\Lib\site-packages\pip\_internal\utils\deprecation.py
.venv\Lib\site-packages\pip\_internal\utils\direct_url_helpers.py
.venv\Lib\site-packages\pip\_internal\utils\egg_link.py
.venv\Lib\site-packages\pip\_internal\utils\entrypoints.py
.venv\Lib\site-packages\pip\_internal\utils\filesystem.py
.venv\Lib\site-packages\pip\_internal\utils\filetypes.py
.venv\Lib\site-packages\pip\_internal\utils\glibc.py
.venv\Lib\site-packages\pip\_internal\utils\hashes.py
.venv\Lib\site-packages\pip\_internal\utils\logging.py
.venv\Lib\site-packages\pip\_internal\utils\misc.py
.venv\Lib\site-packages\pip\_internal\utils\packaging.py
.venv\Lib\site-packages\pip\_internal\utils\pylock.py
.venv\Lib\site-packages\pip\_internal\utils\retry.py
.venv\Lib\site-packages\pip\_internal\utils\subprocess.py
.venv\Lib\site-packages\pip\_internal\utils\temp_dir.py
.venv\Lib\site-packages\pip\_internal\utils\unpacking.py
.venv\Lib\site-packages\pip\_internal\utils\urls.py
.venv\Lib\site-packages\pip\_internal\utils\virtualenv.py
.venv\Lib\site-packages\pip\_internal\utils\wheel.py
.venv\Lib\site-packages\pip\_internal\vcs\__init__.py
.venv\Lib\site-packages\pip\_internal\vcs\bazaar.py
.venv\Lib\site-packages\pip\_internal\vcs\git.py
.venv\Lib\site-packages\pip\_internal\vcs\mercurial.py
.venv\Lib\site-packages\pip\_internal\vcs\subversion.py
.venv\Lib\site-packages\pip\_internal\vcs\versioncontrol.py
.venv\Lib\site-packages\pip\_internal\wheel_builder.py
.venv\Lib\site-packages\pip\_vendor\__init__.py
.venv\Lib\site-packages\pip\_vendor\cachecontrol\__init__.py
.venv\Lib\site-packages\pip\_vendor\cachecontrol\_cmd.py
.venv\Lib\site-packages\pip\_vendor\cachecontrol\adapter.py
.venv\Lib\site-packages\pip\_vendor\cachecontrol\cache.py
.venv\Lib\site-packages\pip\_vendor\cachecontrol\caches\__init__.py
.venv\Lib\site-packages\pip\_vendor\cachecontrol\caches\file_cache.py
.venv\Lib\site-packages\pip\_vendor\cachecontrol\caches\redis_cache.py
.venv\Lib\site-packages\pip\_vendor\cachecontrol\controller.py
.venv\Lib\site-packages\pip\_vendor\cachecontrol\filewrapper.py
.venv\Lib\site-packages\pip\_vendor\cachecontrol\heuristics.py
.venv\Lib\site-packages\pip\_vendor\cachecontrol\serialize.py
.venv\Lib\site-packages\pip\_vendor\cachecontrol\wrapper.py
.venv\Lib\site-packages\pip\_vendor\certifi\__init__.py
.venv\Lib\site-packages\pip\_vendor\certifi\__main__.py
.venv\Lib\site-packages\pip\_vendor\certifi\core.py
.venv\Lib\site-packages\pip\_vendor\distlib\__init__.py
.venv\Lib\site-packages\pip\_vendor\distlib\compat.py
.venv\Lib\site-packages\pip\_vendor\distlib\resources.py
.venv\Lib\site-packages\pip\_vendor\distlib\scripts.py
.venv\Lib\site-packages\pip\_vendor\distlib\util.py
.venv\Lib\site-packages\pip\_vendor\distro\__init__.py
.venv\Lib\site-packages\pip\_vendor\distro\__main__.py
.venv\Lib\site-packages\pip\_vendor\distro\distro.py
.venv\Lib\site-packages\pip\_vendor\idna\__init__.py
.venv\Lib\site-packages\pip\_vendor\idna\__main__.py
.venv\Lib\site-packages\pip\_vendor\idna\cli.py
.venv\Lib\site-packages\pip\_vendor\idna\codec.py
.venv\Lib\site-packages\pip\_vendor\idna\compat.py
.venv\Lib\site-packages\pip\_vendor\idna\core.py
.venv\Lib\site-packages\pip\_vendor\idna\idnadata.py
.venv\Lib\site-packages\pip\_vendor\idna\intranges.py
.venv\Lib\site-packages\pip\_vendor\idna\package_data.py
.venv\Lib\site-packages\pip\_vendor\idna\uts46data.py
.venv\Lib\site-packages\pip\_vendor\msgpack\__init__.py
.venv\Lib\site-packages\pip\_vendor\msgpack\exceptions.py
.venv\Lib\site-packages\pip\_vendor\msgpack\ext.py
.venv\Lib\site-packages\pip\_vendor\msgpack\fallback.py
.venv\Lib\site-packages\pip\_vendor\packaging\__init__.py
.venv\Lib\site-packages\pip\_vendor\packaging\_elffile.py
.venv\Lib\site-packages\pip\_vendor\packaging\_manylinux.py
.venv\Lib\site-packages\pip\_vendor\packaging\_musllinux.py
.venv\Lib\site-packages\pip\_vendor\packaging\_parser.py
.venv\Lib\site-packages\pip\_vendor\packaging\_structures.py
.venv\Lib\site-packages\pip\_vendor\packaging\_tokenizer.py
.venv\Lib\site-packages\pip\_vendor\packaging\dependency_groups.py
.venv\Lib\site-packages\pip\_vendor\packaging\direct_url.py
.venv\Lib\site-packages\pip\_vendor\packaging\errors.py
.venv\Lib\site-packages\pip\_vendor\packaging\licenses\__init__.py
.venv\Lib\site-packages\pip\_vendor\packaging\licenses\_spdx.py
.venv\Lib\site-packages\pip\_vendor\packaging\markers.py
.venv\Lib\site-packages\pip\_vendor\packaging\metadata.py
.venv\Lib\site-packages\pip\_vendor\packaging\pylock.py
.venv\Lib\site-packages\pip\_vendor\packaging\requirements.py
.venv\Lib\site-packages\pip\_vendor\packaging\specifiers.py
.venv\Lib\site-packages\pip\_vendor\packaging\tags.py
.venv\Lib\site-packages\pip\_vendor\packaging\utils.py
.venv\Lib\site-packages\pip\_vendor\packaging\version.py
.venv\Lib\site-packages\pip\_vendor\pkg_resources\__init__.py
.venv\Lib\site-packages\pip\_vendor\platformdirs\__init__.py
.venv\Lib\site-packages\pip\_vendor\platformdirs\__main__.py
.venv\Lib\site-packages\pip\_vendor\platformdirs\_xdg.py
.venv\Lib\site-packages\pip\_vendor\platformdirs\android.py
.venv\Lib\site-packages\pip\_vendor\platformdirs\api.py
.venv\Lib\site-packages\pip\_vendor\platformdirs\macos.py
.venv\Lib\site-packages\pip\_vendor\platformdirs\unix.py
.venv\Lib\site-packages\pip\_vendor\platformdirs\version.py
.venv\Lib\site-packages\pip\_vendor\platformdirs\windows.py
.venv\Lib\site-packages\pip\_vendor\pygments\__init__.py
.venv\Lib\site-packages\pip\_vendor\pygments\__main__.py
.venv\Lib\site-packages\pip\_vendor\pygments\console.py
.venv\Lib\site-packages\pip\_vendor\pygments\filter.py
.venv\Lib\site-packages\pip\_vendor\pygments\filters\__init__.py
.venv\Lib\site-packages\pip\_vendor\pygments\formatter.py
.venv\Lib\site-packages\pip\_vendor\pygments\formatters\__init__.py
.venv\Lib\site-packages\pip\_vendor\pygments\formatters\_mapping.py
.venv\Lib\site-packages\pip\_vendor\pygments\lexer.py
.venv\Lib\site-packages\pip\_vendor\pygments\lexers\__init__.py
.venv\Lib\site-packages\pip\_vendor\pygments\lexers\_mapping.py
.venv\Lib\site-packages\pip\_vendor\pygments\lexers\python.py
.venv\Lib\site-packages\pip\_vendor\pygments\modeline.py
.venv\Lib\site-packages\pip\_vendor\pygments\plugin.py
.venv\Lib\site-packages\pip\_vendor\pygments\regexopt.py
.venv\Lib\site-packages\pip\_vendor\pygments\scanner.py
.venv\Lib\site-packages\pip\_vendor\pygments\sphinxext.py
.venv\Lib\site-packages\pip\_vendor\pygments\style.py
.venv\Lib\site-packages\pip\_vendor\pygments\styles\__init__.py
.venv\Lib\site-packages\pip\_vendor\pygments\styles\_mapping.py
.venv\Lib\site-packages\pip\_vendor\pygments\token.py
.venv\Lib\site-packages\pip\_vendor\pygments\unistring.py
.venv\Lib\site-packages\pip\_vendor\pygments\util.py
.venv\Lib\site-packages\pip\_vendor\pyproject_hooks\__init__.py
.venv\Lib\site-packages\pip\_vendor\pyproject_hooks\_impl.py
.venv\Lib\site-packages\pip\_vendor\pyproject_hooks\_in_process\__init__.py
.venv\Lib\site-packages\pip\_vendor\pyproject_hooks\_in_process\_in_process.py
.venv\Lib\site-packages\pip\_vendor\requests\__init__.py
.venv\Lib\site-packages\pip\_vendor\requests\__version__.py
.venv\Lib\site-packages\pip\_vendor\requests\_internal_utils.py
.venv\Lib\site-packages\pip\_vendor\requests\_types.py
.venv\Lib\site-packages\pip\_vendor\requests\adapters.py
.venv\Lib\site-packages\pip\_vendor\requests\api.py
.venv\Lib\site-packages\pip\_vendor\requests\auth.py
.venv\Lib\site-packages\pip\_vendor\requests\certs.py
.venv\Lib\site-packages\pip\_vendor\requests\compat.py
.venv\Lib\site-packages\pip\_vendor\requests\cookies.py
.venv\Lib\site-packages\pip\_vendor\requests\exceptions.py
.venv\Lib\site-packages\pip\_vendor\requests\help.py
.venv\Lib\site-packages\pip\_vendor\requests\hooks.py
.venv\Lib\site-packages\pip\_vendor\requests\models.py
.venv\Lib\site-packages\pip\_vendor\requests\packages.py
.venv\Lib\site-packages\pip\_vendor\requests\sessions.py
.venv\Lib\site-packages\pip\_vendor\requests\status_codes.py
.venv\Lib\site-packages\pip\_vendor\requests\structures.py
.venv\Lib\site-packages\pip\_vendor\requests\utils.py
.venv\Lib\site-packages\pip\_vendor\resolvelib\__init__.py
.venv\Lib\site-packages\pip\_vendor\resolvelib\providers.py
.venv\Lib\site-packages\pip\_vendor\resolvelib\reporters.py
.venv\Lib\site-packages\pip\_vendor\resolvelib\resolvers\__init__.py
.venv\Lib\site-packages\pip\_vendor\resolvelib\resolvers\abstract.py
.venv\Lib\site-packages\pip\_vendor\resolvelib\resolvers\criterion.py
.venv\Lib\site-packages\pip\_vendor\resolvelib\resolvers\exceptions.py
.venv\Lib\site-packages\pip\_vendor\resolvelib\resolvers\resolution.py
.venv\Lib\site-packages\pip\_vendor\resolvelib\structs.py
.venv\Lib\site-packages\pip\_vendor\rich\__init__.py
.venv\Lib\site-packages\pip\_vendor\rich\__main__.py
.venv\Lib\site-packages\pip\_vendor\rich\_cell_widths.py
.venv\Lib\site-packages\pip\_vendor\rich\_emoji_codes.py
.venv\Lib\site-packages\pip\_vendor\rich\_emoji_replace.py
.venv\Lib\site-packages\pip\_vendor\rich\_export_format.py
.venv\Lib\site-packages\pip\_vendor\rich\_extension.py
.venv\Lib\site-packages\pip\_vendor\rich\_fileno.py
.venv\Lib\site-packages\pip\_vendor\rich\_inspect.py
.venv\Lib\site-packages\pip\_vendor\rich\_log_render.py
.venv\Lib\site-packages\pip\_vendor\rich\_loop.py
.venv\Lib\site-packages\pip\_vendor\rich\_null_file.py
.venv\Lib\site-packages\pip\_vendor\rich\_palettes.py
.venv\Lib\site-packages\pip\_vendor\rich\_pick.py
.venv\Lib\site-packages\pip\_vendor\rich\_ratio.py
.venv\Lib\site-packages\pip\_vendor\rich\_spinners.py
.venv\Lib\site-packages\pip\_vendor\rich\_stack.py
.venv\Lib\site-packages\pip\_vendor\rich\_timer.py
.venv\Lib\site-packages\pip\_vendor\rich\_win32_console.py
.venv\Lib\site-packages\pip\_vendor\rich\_windows.py
.venv\Lib\site-packages\pip\_vendor\rich\_windows_renderer.py
.venv\Lib\site-packages\pip\_vendor\rich\_wrap.py
.venv\Lib\site-packages\pip\_vendor\rich\abc.py
.venv\Lib\site-packages\pip\_vendor\rich\align.py
.venv\Lib\site-packages\pip\_vendor\rich\ansi.py
.venv\Lib\site-packages\pip\_vendor\rich\bar.py
.venv\Lib\site-packages\pip\_vendor\rich\box.py
.venv\Lib\site-packages\pip\_vendor\rich\cells.py
.venv\Lib\site-packages\pip\_vendor\rich\color.py
.venv\Lib\site-packages\pip\_vendor\rich\color_triplet.py
.venv\Lib\site-packages\pip\_vendor\rich\columns.py
.venv\Lib\site-packages\pip\_vendor\rich\console.py
.venv\Lib\site-packages\pip\_vendor\rich\constrain.py
.venv\Lib\site-packages\pip\_vendor\rich\containers.py
.venv\Lib\site-packages\pip\_vendor\rich\control.py
.venv\Lib\site-packages\pip\_vendor\rich\default_styles.py
.venv\Lib\site-packages\pip\_vendor\rich\diagnose.py
.venv\Lib\site-packages\pip\_vendor\rich\emoji.py
.venv\Lib\site-packages\pip\_vendor\rich\errors.py
.venv\Lib\site-packages\pip\_vendor\rich\file_proxy.py
.venv\Lib\site-packages\pip\_vendor\rich\filesize.py
.venv\Lib\site-packages\pip\_vendor\rich\highlighter.py
.venv\Lib\site-packages\pip\_vendor\rich\json.py
.venv\Lib\site-packages\pip\_vendor\rich\jupyter.py
.venv\Lib\site-packages\pip\_vendor\rich\layout.py
.venv\Lib\site-packages\pip\_vendor\rich\live.py
.venv\Lib\site-packages\pip\_vendor\rich\live_render.py
.venv\Lib\site-packages\pip\_vendor\rich\logging.py
.venv\Lib\site-packages\pip\_vendor\rich\markup.py
.venv\Lib\site-packages\pip\_vendor\rich\measure.py
.venv\Lib\site-packages\pip\_vendor\rich\padding.py
.venv\Lib\site-packages\pip\_vendor\rich\pager.py
.venv\Lib\site-packages\pip\_vendor\rich\palette.py
.venv\Lib\site-packages\pip\_vendor\rich\panel.py
.venv\Lib\site-packages\pip\_vendor\rich\pretty.py
.venv\Lib\site-packages\pip\_vendor\rich\progress.py
.venv\Lib\site-packages\pip\_vendor\rich\progress_bar.py
.venv\Lib\site-packages\pip\_vendor\rich\prompt.py
.venv\Lib\site-packages\pip\_vendor\rich\protocol.py
.venv\Lib\site-packages\pip\_vendor\rich\region.py
.venv\Lib\site-packages\pip\_vendor\rich\repr.py
.venv\Lib\site-packages\pip\_vendor\rich\rule.py
.venv\Lib\site-packages\pip\_vendor\rich\scope.py
.venv\Lib\site-packages\pip\_vendor\rich\screen.py
.venv\Lib\site-packages\pip\_vendor\rich\segment.py
.venv\Lib\site-packages\pip\_vendor\rich\spinner.py
.venv\Lib\site-packages\pip\_vendor\rich\status.py
.venv\Lib\site-packages\pip\_vendor\rich\style.py
.venv\Lib\site-packages\pip\_vendor\rich\styled.py
.venv\Lib\site-packages\pip\_vendor\rich\syntax.py
.venv\Lib\site-packages\pip\_vendor\rich\table.py
.venv\Lib\site-packages\pip\_vendor\rich\terminal_theme.py
.venv\Lib\site-packages\pip\_vendor\rich\text.py
.venv\Lib\site-packages\pip\_vendor\rich\theme.py
.venv\Lib\site-packages\pip\_vendor\rich\themes.py
.venv\Lib\site-packages\pip\_vendor\rich\traceback.py
.venv\Lib\site-packages\pip\_vendor\rich\tree.py
.venv\Lib\site-packages\pip\_vendor\tomli\__init__.py
.venv\Lib\site-packages\pip\_vendor\tomli\_parser.py
.venv\Lib\site-packages\pip\_vendor\tomli\_re.py
.venv\Lib\site-packages\pip\_vendor\tomli\_types.py
.venv\Lib\site-packages\pip\_vendor\tomli_w\__init__.py
.venv\Lib\site-packages\pip\_vendor\tomli_w\_writer.py
.venv\Lib\site-packages\pip\_vendor\truststore\__init__.py
.venv\Lib\site-packages\pip\_vendor\truststore\_api.py
.venv\Lib\site-packages\pip\_vendor\truststore\_macos.py
.venv\Lib\site-packages\pip\_vendor\truststore\_openssl.py
.venv\Lib\site-packages\pip\_vendor\truststore\_ssl_constants.py
.venv\Lib\site-packages\pip\_vendor\truststore\_windows.py
.venv\Lib\site-packages\pip\_vendor\urllib3\__init__.py
.venv\Lib\site-packages\pip\_vendor\urllib3\_base_connection.py
.venv\Lib\site-packages\pip\_vendor\urllib3\_collections.py
.venv\Lib\site-packages\pip\_vendor\urllib3\_request_methods.py
.venv\Lib\site-packages\pip\_vendor\urllib3\_version.py
.venv\Lib\site-packages\pip\_vendor\urllib3\connection.py
.venv\Lib\site-packages\pip\_vendor\urllib3\connectionpool.py
.venv\Lib\site-packages\pip\_vendor\urllib3\contrib\__init__.py
.venv\Lib\site-packages\pip\_vendor\urllib3\contrib\emscripten\__init__.py
.venv\Lib\site-packages\pip\_vendor\urllib3\contrib\emscripten\connection.py
.venv\Lib\site-packages\pip\_vendor\urllib3\contrib\emscripten\fetch.py
.venv\Lib\site-packages\pip\_vendor\urllib3\contrib\emscripten\request.py
.venv\Lib\site-packages\pip\_vendor\urllib3\contrib\emscripten\response.py
.venv\Lib\site-packages\pip\_vendor\urllib3\contrib\pyopenssl.py
.venv\Lib\site-packages\pip\_vendor\urllib3\contrib\socks.py
.venv\Lib\site-packages\pip\_vendor\urllib3\exceptions.py
.venv\Lib\site-packages\pip\_vendor\urllib3\fields.py
.venv\Lib\site-packages\pip\_vendor\urllib3\filepost.py
.venv\Lib\site-packages\pip\_vendor\urllib3\http2\__init__.py
.venv\Lib\site-packages\pip\_vendor\urllib3\http2\connection.py
.venv\Lib\site-packages\pip\_vendor\urllib3\http2\probe.py
.venv\Lib\site-packages\pip\_vendor\urllib3\poolmanager.py
.venv\Lib\site-packages\pip\_vendor\urllib3\response.py
.venv\Lib\site-packages\pip\_vendor\urllib3\util\__init__.py
.venv\Lib\site-packages\pip\_vendor\urllib3\util\connection.py
.venv\Lib\site-packages\pip\_vendor\urllib3\util\proxy.py
.venv\Lib\site-packages\pip\_vendor\urllib3\util\request.py
.venv\Lib\site-packages\pip\_vendor\urllib3\util\response.py
.venv\Lib\site-packages\pip\_vendor\urllib3\util\retry.py
.venv\Lib\site-packages\pip\_vendor\urllib3\util\ssl_.py
.venv\Lib\site-packages\pip\_vendor\urllib3\util\ssl_match_hostname.py
.venv\Lib\site-packages\pip\_vendor\urllib3\util\ssltransport.py
.venv\Lib\site-packages\pip\_vendor\urllib3\util\timeout.py
.venv\Lib\site-packages\pip\_vendor\urllib3\util\url.py
.venv\Lib\site-packages\pip\_vendor\urllib3\util\util.py
.venv\Lib\site-packages\pip\_vendor\urllib3\util\wait.py
.venv\Lib\site-packages\pygame\__briefcase\__init__.py
.venv\Lib\site-packages\pygame\__briefcase\pygame_ce.py
.venv\Lib\site-packages\pygame\__init__.py
.venv\Lib\site-packages\pygame\__pyinstaller\__init__.py
.venv\Lib\site-packages\pygame\__pyinstaller\hook-pygame.py
.venv\Lib\site-packages\pygame\_camera_opencv.py
.venv\Lib\site-packages\pygame\_data_classes.py
.venv\Lib\site-packages\pygame\_debug.py
.venv\Lib\site-packages\pygame\_sdl2\__init__.py
.venv\Lib\site-packages\pygame\_sdl2\window.py
.venv\Lib\site-packages\pygame\_sprite.py
.venv\Lib\site-packages\pygame\camera.py
.venv\Lib\site-packages\pygame\colordict.py
.venv\Lib\site-packages\pygame\cursors.py
.venv\Lib\site-packages\pygame\docs\__init__.py
.venv\Lib\site-packages\pygame\docs\__main__.py
.venv\Lib\site-packages\pygame\docs\serve.py
.venv\Lib\site-packages\pygame\docs\static.py
.venv\Lib\site-packages\pygame\examples\__init__.py
.venv\Lib\site-packages\pygame\examples\aacircle.py
.venv\Lib\site-packages\pygame\examples\aliens.py
.venv\Lib\site-packages\pygame\examples\arraydemo.py
.venv\Lib\site-packages\pygame\examples\audiocapture.py
.venv\Lib\site-packages\pygame\examples\blend_fill.py
.venv\Lib\site-packages\pygame\examples\blit_blends.py
.venv\Lib\site-packages\pygame\examples\camera.py
.venv\Lib\site-packages\pygame\examples\chimp.py
.venv\Lib\site-packages\pygame\examples\cursors.py
.venv\Lib\site-packages\pygame\examples\dropevent.py
.venv\Lib\site-packages\pygame\examples\eventlist.py
.venv\Lib\site-packages\pygame\examples\font_viewer.py
.venv\Lib\site-packages\pygame\examples\fonty.py
.venv\Lib\site-packages\pygame\examples\freetype_misc.py
.venv\Lib\site-packages\pygame\examples\glcube.py
.venv\Lib\site-packages\pygame\examples\go_over_there.py
.venv\Lib\site-packages\pygame\examples\headless_no_windows_needed.py
.venv\Lib\site-packages\pygame\examples\joystick.py
.venv\Lib\site-packages\pygame\examples\liquid.py
.venv\Lib\site-packages\pygame\examples\mask.py
.venv\Lib\site-packages\pygame\examples\midi.py
.venv\Lib\site-packages\pygame\examples\moveit.py
.venv\Lib\site-packages\pygame\examples\multiplayer_joystick.py
.venv\Lib\site-packages\pygame\examples\music_drop_fade.py
.venv\Lib\site-packages\pygame\examples\ninepatch.py
.venv\Lib\site-packages\pygame\examples\pixelarray.py
.venv\Lib\site-packages\pygame\examples\playmus.py
.venv\Lib\site-packages\pygame\examples\prevent_display_stretching.py
.venv\Lib\site-packages\pygame\examples\resizing_new.py
.venv\Lib\site-packages\pygame\examples\retro_scaling.py
.venv\Lib\site-packages\pygame\examples\scaletest.py
.venv\Lib\site-packages\pygame\examples\scrap_clipboard.py
.venv\Lib\site-packages\pygame\examples\scroll.py
.venv\Lib\site-packages\pygame\examples\setmodescale.py
.venv\Lib\site-packages\pygame\examples\sound.py
.venv\Lib\site-packages\pygame\examples\sound_array_demos.py
.venv\Lib\site-packages\pygame\examples\sprite_texture.py
.venv\Lib\site-packages\pygame\examples\stars.py
.venv\Lib\site-packages\pygame\examples\testsprite.py
.venv\Lib\site-packages\pygame\examples\textinput.py
.venv\Lib\site-packages\pygame\examples\vgrade.py
.venv\Lib\site-packages\pygame\examples\video.py
.venv\Lib\site-packages\pygame\examples\window_opengl.py
.venv\Lib\site-packages\pygame\freetype.py
.venv\Lib\site-packages\pygame\ftfont.py
.venv\Lib\site-packages\pygame\locals.py
.venv\Lib\site-packages\pygame\macosx.py
.venv\Lib\site-packages\pygame\midi.py
.venv\Lib\site-packages\pygame\pkgdata.py
.venv\Lib\site-packages\pygame\sndarray.py
.venv\Lib\site-packages\pygame\sprite.py
.venv\Lib\site-packages\pygame\surfarray.py
.venv\Lib\site-packages\pygame\sysfont.py
.venv\Lib\site-packages\pygame\tests\__init__.py
.venv\Lib\site-packages\pygame\tests\__main__.py
.venv\Lib\site-packages\pygame\tests\base_test.py
.venv\Lib\site-packages\pygame\tests\blit_test.py
.venv\Lib\site-packages\pygame\tests\bufferproxy_test.py
.venv\Lib\site-packages\pygame\tests\camera_test.py
.venv\Lib\site-packages\pygame\tests\color_test.py
.venv\Lib\site-packages\pygame\tests\constants_test.py
.venv\Lib\site-packages\pygame\tests\controller_test.py
.venv\Lib\site-packages\pygame\tests\ctest_test.py
.venv\Lib\site-packages\pygame\tests\cursors_test.py
.venv\Lib\site-packages\pygame\tests\debug_test.py
.venv\Lib\site-packages\pygame\tests\display_test.py
.venv\Lib\site-packages\pygame\tests\docs_test.py
.venv\Lib\site-packages\pygame\tests\draw_test.py
.venv\Lib\site-packages\pygame\tests\event_test.py
.venv\Lib\site-packages\pygame\tests\font_test.py
.venv\Lib\site-packages\pygame\tests\freetype_test.py
.venv\Lib\site-packages\pygame\tests\ftfont_test.py
.venv\Lib\site-packages\pygame\tests\geometry_test.py
.venv\Lib\site-packages\pygame\tests\gfxdraw_test.py
.venv\Lib\site-packages\pygame\tests\image__save_gl_surface_test.py
.venv\Lib\site-packages\pygame\tests\image_test.py
.venv\Lib\site-packages\pygame\tests\imageext_test.py
.venv\Lib\site-packages\pygame\tests\joystick_test.py
.venv\Lib\site-packages\pygame\tests\key_test.py
.venv\Lib\site-packages\pygame\tests\locals_test.py
.venv\Lib\site-packages\pygame\tests\mask_test.py
.venv\Lib\site-packages\pygame\tests\math_test.py
.venv\Lib\site-packages\pygame\tests\midi_test.py
.venv\Lib\site-packages\pygame\tests\mixer_music_test.py
.venv\Lib\site-packages\pygame\tests\mixer_test.py
.venv\Lib\site-packages\pygame\tests\mouse_test.py
.venv\Lib\site-packages\pygame\tests\pixelarray_test.py
.venv\Lib\site-packages\pygame\tests\pixelcopy_test.py
.venv\Lib\site-packages\pygame\tests\rect_test.py
.venv\Lib\site-packages\pygame\tests\render_test.py
.venv\Lib\site-packages\pygame\tests\rwobject_test.py
.venv\Lib\site-packages\pygame\tests\scrap_test.py
.venv\Lib\site-packages\pygame\tests\sndarray_tags.py
.venv\Lib\site-packages\pygame\tests\sndarray_test.py
.venv\Lib\site-packages\pygame\tests\sprite_test.py
.venv\Lib\site-packages\pygame\tests\surface_test.py
.venv\Lib\site-packages\pygame\tests\surfarray_tags.py
.venv\Lib\site-packages\pygame\tests\surfarray_test.py
.venv\Lib\site-packages\pygame\tests\surflock_test.py
.venv\Lib\site-packages\pygame\tests\sysfont_test.py
.venv\Lib\site-packages\pygame\tests\system_test.py
.venv\Lib\site-packages\pygame\tests\test_utils\__init__.py
.venv\Lib\site-packages\pygame\tests\test_utils\arrinter.py
.venv\Lib\site-packages\pygame\tests\test_utils\async_sub.py
.venv\Lib\site-packages\pygame\tests\test_utils\buftools.py
.venv\Lib\site-packages\pygame\tests\test_utils\png.py
.venv\Lib\site-packages\pygame\tests\test_utils\run_tests.py
.venv\Lib\site-packages\pygame\tests\test_utils\test_machinery.py
.venv\Lib\site-packages\pygame\tests\test_utils\test_runner.py
.venv\Lib\site-packages\pygame\tests\time_test.py
.venv\Lib\site-packages\pygame\tests\touch_test.py
.venv\Lib\site-packages\pygame\tests\transform_test.py
.venv\Lib\site-packages\pygame\tests\typing_test.py
.venv\Lib\site-packages\pygame\tests\version_test.py
.venv\Lib\site-packages\pygame\tests\video_test.py
.venv\Lib\site-packages\pygame\tests\window_test.py
.venv\Lib\site-packages\pygame\typing.py
.venv\Lib\site-packages\pygame\version.py
.venv\Lib\site-packages\PySide6\__init__.py
.venv\Lib\site-packages\PySide6\_config.py
.venv\Lib\site-packages\PySide6\_git_pyside_version.py
.venv\Lib\site-packages\PySide6\QtAsyncio\__init__.py
.venv\Lib\site-packages\PySide6\QtAsyncio\events.py
.venv\Lib\site-packages\PySide6\QtAsyncio\futures.py
.venv\Lib\site-packages\PySide6\QtAsyncio\tasks.py
.venv\Lib\site-packages\PySide6\scripts\__init__.py
.venv\Lib\site-packages\PySide6\scripts\deploy.py
.venv\Lib\site-packages\PySide6\scripts\deploy_lib\__init__.py
.venv\Lib\site-packages\PySide6\scripts\deploy_lib\commands.py
.venv\Lib\site-packages\PySide6\scripts\deploy_lib\config.py
.venv\Lib\site-packages\PySide6\scripts\deploy_lib\dependency_util.py
.venv\Lib\site-packages\PySide6\scripts\deploy_lib\deploy_util.py
.venv\Lib\site-packages\PySide6\scripts\deploy_lib\nuitka_helper.py
.venv\Lib\site-packages\PySide6\scripts\deploy_lib\python_helper.py
.venv\Lib\site-packages\PySide6\scripts\metaobjectdump.py
.venv\Lib\site-packages\PySide6\scripts\project.py
.venv\Lib\site-packages\PySide6\scripts\project_lib\__init__.py
.venv\Lib\site-packages\PySide6\scripts\project_lib\design_studio_project.py
.venv\Lib\site-packages\PySide6\scripts\project_lib\newproject.py
.venv\Lib\site-packages\PySide6\scripts\project_lib\project_data.py
.venv\Lib\site-packages\PySide6\scripts\project_lib\pyproject_json.py
.venv\Lib\site-packages\PySide6\scripts\project_lib\pyproject_parse_result.py
.venv\Lib\site-packages\PySide6\scripts\project_lib\pyproject_toml.py
.venv\Lib\site-packages\PySide6\scripts\project_lib\utils.py
.venv\Lib\site-packages\PySide6\scripts\pyside_tool.py
.venv\Lib\site-packages\PySide6\scripts\qml.py
.venv\Lib\site-packages\PySide6\scripts\qtpy2cpp.py
.venv\Lib\site-packages\PySide6\scripts\qtpy2cpp_lib\astdump.py
.venv\Lib\site-packages\PySide6\scripts\qtpy2cpp_lib\formatter.py
.venv\Lib\site-packages\PySide6\scripts\qtpy2cpp_lib\nodedump.py
.venv\Lib\site-packages\PySide6\scripts\qtpy2cpp_lib\qt.py
.venv\Lib\site-packages\PySide6\scripts\qtpy2cpp_lib\tokenizer.py
.venv\Lib\site-packages\PySide6\scripts\qtpy2cpp_lib\visitor.py
.venv\Lib\site-packages\PySide6\support\__init__.py
.venv\Lib\site-packages\PySide6\support\deprecated.py
.venv\Lib\site-packages\PySide6\support\generate_pyi.py
.venv\Lib\site-packages\requests\__init__.py
.venv\Lib\site-packages\requests\__version__.py
.venv\Lib\site-packages\requests\_internal_utils.py
.venv\Lib\site-packages\requests\_types.py
.venv\Lib\site-packages\requests\adapters.py
.venv\Lib\site-packages\requests\api.py
.venv\Lib\site-packages\requests\auth.py
.venv\Lib\site-packages\requests\certs.py
.venv\Lib\site-packages\requests\compat.py
.venv\Lib\site-packages\requests\cookies.py
.venv\Lib\site-packages\requests\exceptions.py
.venv\Lib\site-packages\requests\help.py
.venv\Lib\site-packages\requests\hooks.py
.venv\Lib\site-packages\requests\models.py
.venv\Lib\site-packages\requests\packages.py
.venv\Lib\site-packages\requests\sessions.py
.venv\Lib\site-packages\requests\status_codes.py
.venv\Lib\site-packages\requests\structures.py
.venv\Lib\site-packages\requests\utils.py
.venv\Lib\site-packages\shiboken6\__init__.py
.venv\Lib\site-packages\shiboken6\_config.py
.venv\Lib\site-packages\shiboken6\_git_shiboken_module_version.py
.venv\Lib\site-packages\urllib3\__init__.py
.venv\Lib\site-packages\urllib3\_base_connection.py
.venv\Lib\site-packages\urllib3\_collections.py
.venv\Lib\site-packages\urllib3\_request_methods.py
.venv\Lib\site-packages\urllib3\_version.py
.venv\Lib\site-packages\urllib3\connection.py
.venv\Lib\site-packages\urllib3\connectionpool.py
.venv\Lib\site-packages\urllib3\contrib\__init__.py
.venv\Lib\site-packages\urllib3\contrib\emscripten\__init__.py
.venv\Lib\site-packages\urllib3\contrib\emscripten\connection.py
.venv\Lib\site-packages\urllib3\contrib\emscripten\fetch.py
.venv\Lib\site-packages\urllib3\contrib\emscripten\request.py
.venv\Lib\site-packages\urllib3\contrib\emscripten\response.py
.venv\Lib\site-packages\urllib3\contrib\pyopenssl.py
.venv\Lib\site-packages\urllib3\contrib\socks.py
.venv\Lib\site-packages\urllib3\exceptions.py
.venv\Lib\site-packages\urllib3\fields.py
.venv\Lib\site-packages\urllib3\filepost.py
.venv\Lib\site-packages\urllib3\http2\__init__.py
.venv\Lib\site-packages\urllib3\http2\connection.py
.venv\Lib\site-packages\urllib3\http2\probe.py
.venv\Lib\site-packages\urllib3\poolmanager.py
.venv\Lib\site-packages\urllib3\response.py
.venv\Lib\site-packages\urllib3\util\__init__.py
.venv\Lib\site-packages\urllib3\util\connection.py
.venv\Lib\site-packages\urllib3\util\proxy.py
.venv\Lib\site-packages\urllib3\util\request.py
.venv\Lib\site-packages\urllib3\util\response.py
.venv\Lib\site-packages\urllib3\util\retry.py
.venv\Lib\site-packages\urllib3\util\ssl_.py
.venv\Lib\site-packages\urllib3\util\ssl_match_hostname.py
.venv\Lib\site-packages\urllib3\util\ssltransport.py
.venv\Lib\site-packages\urllib3\util\timeout.py
.venv\Lib\site-packages\urllib3\util\url.py
.venv\Lib\site-packages\urllib3\util\util.py
.venv\Lib\site-packages\urllib3\util\wait.py
build.py
config.py
core\__init__.py
core\api.py
core\autostart.py
core\i18n.py
core\image_loader.py
core\images.py
core\network.py
core\paths.py
core\scrapers\__init__.py
core\scrapers\store_scrapers.py
core\steam_enricher.py
core\storage.py
core\translator.py
core\tray.py
core\ui_settings.py
core\validators.py
logger.py
main.py
scripts\clean_release.py
tests\__init__.py
tests\test_history.py
tests\test_integration_e2e.py
tests\test_phase1_p0.py
tests\test_phase2_p1.py
tests\test_phase3_ux.py
ui\__init__.py
ui\components\game_card.py
ui\components\notification_toast.py
ui\components\store_widget.py
ui\design_system.py
ui\main_window.py
ui\main_window_audio.py
ui\main_window_games.py
ui\main_window_helpers.py
ui\main_window_history.py
ui\main_window_navigation.py
ui\main_window_theme.py
ui\main_window_tray.py
ui\main_window_ui.py
ui\modals\kofi_modal.py
ui\modals\settings_modal.py
```


## 3. File inventory

### Extension counts

```text

Count Name          
----- ----          
 1301 .png          
 1217 .pyc          
 1211 .py           
 1008 .qml          
  394 .pyi          
  368 .dll          
  304 .qm           
  194 .h            
  187               
  138 .json         
  131 .pyd          
  104 .qmltypes     
  101 .xml          
   87 .txt          
   82 .html         
   62 .f90          
   61 .pak          
   53 .exe          
   36 .webp         
   30 .csv          
   29 .cpp          
   26 .lib          
   25 .f            
   25 .typed        
   17 .md           
   15 .jpg          
   11 .metainfo     
   11 .js           
   11 .cmake        
   10 .log          
   10 .rst          
   10 .gif          
    9 .bak          
    8 .pyf          
    7 .svg          
    7 .pxd          
    7 .wav          
    6 .css          
    5 .npy          
    5 .c            
    4 .ttf          
    4 .pyx          
    4 .obj          
    3 .bdf          
    3 .ico          
    3 .gz           
    3 .anim_fix_bak 
    3 .build        
    2 .ps1          
    2 .mp3          
    2 .tif          
    2 .bin          
    2 .prl          
    2 .xbm          
    2 .frag         
    2 .otf          
    2 .npz          
    2 .bmp          
    2 .f2py_f2cmap  
    2 .zip          
    2 .bak2         
    2 .gitignore    
    2 .pem          
    2 .cfg          
    2 .spec         
    1 .fits         
    1 .ini          
    1 .pc           
    1 .pkl          
    1 .mesh         
    1 .gitkeep      
    1 .inc          
    1 .gitattributes
    1 .bak_signal   
    1 .template     
    1 .dat          
    1 .icns         
    1 .f95          
    1 .wv           
    1 .opus         
    1 .mid          
    1 .lbm          
    1 .ogg          
    1 .pgm          
    1 .pcx          
    1 .pnm          
    1 .flac         
    1 .ppm          
    1 .sfd          
    1 .tga          
    1 .APACHE       
    1 .BSD          
    1 .pbm          
    1 .xpm          
    1 .qoi          
    1 .xcf          
    1 .xm
```

### Largest project files

```text

    MB FullName                                                                          
    -- --------                                                                          
194,02 F:\KURIGAMESDEV\KG TRACKER\.venv\Lib\site-packages\PySide6\Qt6WebEngineCore.dll   
 72,33 F:\KURIGAMESDEV\KG TRACKER\.venv\Lib\site-packages\PySide6\resources\qtwebengin...
 20,93 F:\KURIGAMESDEV\KG TRACKER\assets\chill.wav                                       
 19,68 F:\KURIGAMESDEV\KG TRACKER\.venv\Lib\site-packages\PySide6\opengl32sw.dll         
 19,64 F:\KURIGAMESDEV\KG TRACKER\.venv\Lib\site-packages\numpy.libs\libscipy_openblas...
 13,41 F:\KURIGAMESDEV\KG TRACKER\.venv\Lib\site-packages\PySide6\avcodec-61.dll         
 11,07 F:\KURIGAMESDEV\KG TRACKER\.venv\Lib\site-packages\PySide6\resources\qtwebengin...
  9,98 F:\KURIGAMESDEV\KG TRACKER\.venv\Lib\site-packages\PySide6\resources\icudtl.dat   
  9,88 F:\KURIGAMESDEV\KG TRACKER\.venv\Lib\site-packages\PySide6\Qt6Core.dll            
   9,1 F:\KURIGAMESDEV\KG TRACKER\.venv\Lib\site-packages\PySide6\Qt6Gui.dll             
  8,28 F:\KURIGAMESDEV\KG TRACKER\.venv\Lib\site-packages\PySide6\QtOpenGL.pyd           
  7,52 F:\KURIGAMESDEV\KG TRACKER\.venv\Lib\site-packages\PIL\_avif.cp314-win_amd64.pyd  
  6,26 F:\KURIGAMESDEV\KG TRACKER\.venv\Lib\site-packages\PySide6\Qt6Quick.dll           
   6,2 F:\KURIGAMESDEV\KG TRACKER\.venv\Lib\site-packages\PySide6\Qt6Widgets.dll         
  5,09 F:\KURIGAMESDEV\KG TRACKER\.venv\Lib\site-packages\PySide6\Qt6Qml.dll             
  4,99 F:\KURIGAMESDEV\KG TRACKER\.venv\Lib\site-packages\PySide6\Qt6Designer.dll        
  4,63 F:\KURIGAMESDEV\KG TRACKER\.venv\Lib\site-packages\PySide6\QtWidgets.pyd          
  4,41 F:\KURIGAMESDEV\KG TRACKER\.venv\Lib\site-packages\PySide6\Qt6Pdf.dll             
  4,18 F:\KURIGAMESDEV\KG TRACKER\.venv\Lib\site-packages\PySide6\Qt6Quick3DRuntimeRen...
  4,18 F:\KURIGAMESDEV\KG TRACKER\.venv\Lib\site-packages\PySide6\Qt6ShaderTools.dll     
  3,79 F:\KURIGAMESDEV\KG TRACKER\cache\3a6a7bf75d57b15879bb42d10d724ced0092e247fc200f...
  3,72 F:\KURIGAMESDEV\KG TRACKER\.venv\Lib\site-packages\PySide6\QtGui.pyd              
   3,7 F:\KURIGAMESDEV\KG TRACKER\cache\b1e5f7eeebffa47bd0bdfc6bc4c0555f7e380cc8f2a3ff...
  3,69 F:\KURIGAMESDEV\KG TRACKER\.venv\Lib\site-packages\numpy\_core\_multiarray_umat...
  3,56 F:\KURIGAMESDEV\KG TRACKER\.venv\Lib\site-packages\PySide6\qmlls.exe              
  3,19 F:\KURIGAMESDEV\KG TRACKER\.venv\Lib\site-packages\PySide6\QtCore.pyd             
  3,19 F:\KURIGAMESDEV\KG TRACKER\.venv\Lib\site-packages\PySide6\qml\QtQuick\Controls...
  2,96 F:\KURIGAMESDEV\KG TRACKER\.venv\Lib\site-packages\PySide6\Qt6QuickControls2Ima...
   2,8 F:\KURIGAMESDEV\KG TRACKER\assets\branding\KG_LOGO_MASTER_2040.png                
  2,63 F:\KURIGAMESDEV\KG TRACKER\.venv\Lib\site-packages\PySide6\Qt6QuickDialogs2Quic...
  2,53 F:\KURIGAMESDEV\KG TRACKER\.venv\Lib\site-packages\PySide6\avformat-61.dll        
  2,51 F:\KURIGAMESDEV\KG TRACKER\.venv\Lib\site-packages\PIL\_imaging.cp314-win_amd64...
  2,46 F:\KURIGAMESDEV\KG TRACKER\.venv\Lib\site-packages\PySide6\Qt63DRender.dll        
  2,44 F:\KURIGAMESDEV\KG TRACKER\.venv\Lib\site-packages\PySide6\Qt6Graphs.dll          
  2,41 F:\KURIGAMESDEV\KG TRACKER\.venv\Lib\site-packages\PySide6\Qt6QmlCompiler.dll     
  2,33 F:\KURIGAMESDEV\KG TRACKER\.venv\Lib\site-packages\PySide6\resources\v8_context...
  2,33 F:\KURIGAMESDEV\KG TRACKER\.venv\Lib\site-packages\PySide6\Qt6DesignerComponent...
  2,24 F:\KURIGAMESDEV\KG TRACKER\.venv\Lib\site-packages\PySide6\qmlformat.exe          
  2,16 F:\KURIGAMESDEV\KG TRACKER\.venv\Lib\site-packages\PySide6\resources\qtwebengin...
  2,16 F:\KURIGAMESDEV\KG TRACKER\.venv\Lib\site-packages\PySide6\resources\qtwebengin...
```


## 4. Python metrics

Python files: 1211
Python lines: 545587

```text

Lines File                                                                              
----- ----                                                                              
16897 .venv\Lib\site-packages\idna\uts46data.py                                         
16896 .venv\Lib\site-packages\pip\_vendor\idna\uts46data.py                             
11587 .venv\Lib\site-packages\numpy\_core\tests\test_multiarray.py                      
 9006 .venv\Lib\site-packages\numpy\ma\core.py                                          
 7576 .venv\Lib\site-packages\pygame\tests\draw_test.py                                 
 7131 .venv\Lib\site-packages\numpy\_core\_add_newdocs.py                               
 6699 .venv\Lib\site-packages\pygame\tests\mask_test.py                                 
 6171 .venv\Lib\site-packages\numpy\ma\tests\test_core.py                               
 5775 .venv\Lib\site-packages\numpy\lib\_function_base_impl.py                          
 5231 .venv\Lib\site-packages\numpy\_core\tests\test_umath.py                           
 4787 .venv\Lib\site-packages\numpy\lib\tests\test_function_base.py                     
 4388 .venv\Lib\site-packages\pygame\tests\surface_test.py                              
 4385 .venv\Lib\site-packages\PIL\Image.py                                              
 4278 .venv\Lib\site-packages\numpy\_core\tests\test_numeric.py                         
 4271 .venv\Lib\site-packages\numpy\_core\fromnumeric.py                                
 4005 .venv\Lib\site-packages\pygame\tests\test_utils\png.py                            
 3727 .venv\Lib\site-packages\numpy\f2py\crackfortran.py                                
 3690 .venv\Lib\site-packages\numpy\_core\tests\test_nditer.py                          
 3676 .venv\Lib\site-packages\pip\_vendor\pkg_resources\__init__.py                     
 3649 .venv\Lib\site-packages\numpy\linalg\_linalg.py                                   
 3610 .venv\Lib\site-packages\pip\_vendor\rich\_emoji_codes.py                          
 3566 .venv\Lib\site-packages\pygame\tests\rect_test.py                                 
 3459 .venv\Lib\site-packages\numpy\_core\tests\test_ufunc.py                           
 3343 .venv\Lib\site-packages\pygame\tests\math_test.py                                 
 3220 .venv\Lib\site-packages\numpy\_core\tests\test_datetime.py                        
 2918 .venv\Lib\site-packages\numpy\_core\tests\test_stringdtype.py                     
 2899 .venv\Lib\site-packages\numpy\testing\_private\utils.py                           
 2830 .venv\Lib\site-packages\numpy\random\tests\test_generator_mt19937.py              
 2733 .venv\Lib\site-packages\numpy\lib\tests\test_io.py                                
 2707 .venv\Lib\site-packages\numpy\_core\numeric.py                                    
 2680 .venv\Lib\site-packages\pip\_vendor\rich\console.py                               
 2672 .venv\Lib\site-packages\numpy\_core\tests\test_regression.py                      
 2496 .venv\Lib\site-packages\charset_normalizer\constant.py                            
 2492 .venv\Lib\site-packages\numpy\linalg\tests\test_linalg.py                         
 2491 .venv\Lib\site-packages\numpy\lib\_npyio_impl.py                                  
 2354 .venv\Lib\site-packages\PIL\TiffImagePlugin.py                                    
 2266 .venv\Lib\site-packages\numpy\ma\extras.py                                        
 2253 .venv\Lib\site-packages\pygame\tests\geometry_test.py                             
 2232 .venv\Lib\site-packages\pygame\tests\transform_test.py                            
 2147 .venv\Lib\site-packages\numpy\testing\tests\test_utils.py                         
 2107 .venv\Lib\site-packages\numpy\random\tests\test_randomstate.py                    
 2107 .venv\Lib\site-packages\numpy\_core\tests\test_dtype.py                           
 2053 .venv\Lib\site-packages\numpy\polynomial\chebyshev.py                             
 2021 .venv\Lib\site-packages\pip\_vendor\distlib\util.py                               
 2006 .venv\Lib\site-packages\numpy\lib\_nanfunctions_impl.py                           
 1945 .venv\Lib\site-packages\numpy\ma\tests\test_extras.py                             
 1943 .venv\Lib\site-packages\pip\_vendor\packaging\specifiers.py                       
 1897 .venv\Lib\site-packages\pip\_vendor\idna\idnadata.py                              
 1897 .venv\Lib\site-packages\idna\idnadata.py                                          
 1813 .venv\Lib\site-packages\numpy\_core\strings.py                                    
 1810 .venv\Lib\site-packages\pygame\tests\freetype_test.py                             
 1794 .venv\Lib\site-packages\numpy\polynomial\hermite.py                               
 1788 .venv\Lib\site-packages\pygame\sprite.py                                          
 1788 .venv\Lib\site-packages\numpy\_core\arrayprint.py                                 
 1767 .venv\Lib\site-packages\pygame\tests\pixelarray_test.py                           
 1743 .venv\Lib\site-packages\numpy\_core\multiarray.py                                 
 1729 .venv\Lib\site-packages\numpy\polynomial\laguerre.py                              
 1723 .venv\Lib\site-packages\numpy\random\tests\test_random.py                         
 1717 .venv\Lib\site-packages\numpy\_core\tests\test_indexing.py                        
 1715 .venv\Lib\site-packages\pip\_vendor\rich\progress.py                              
 1693 .venv\Lib\site-packages\numpy\fft\_pocketfft.py                                   
 1692 .venv\Lib\site-packages\numpy\polynomial\hermite_e.py                             
 1683 .venv\Lib\site-packages\numpy\polynomial\polynomial.py                            
 1681 .venv\Lib\site-packages\numpy\lib\recfunctions.py                                 
 1655 .venv\Lib\site-packages\numpy\polynomial\legendre.py                              
 1647 .venv\Lib\site-packages\numpy\_core\einsumfunc.py                                 
 1641 .venv\Lib\site-packages\numpy\f2py\rules.py                                       
 1593 .venv\Lib\site-packages\pygame\tests\color_test.py                                
 1579 .venv\Lib\site-packages\numpy\f2py\cfuncs.py                                      
 1578 .venv\Lib\site-packages\PIL\PngImagePlugin.py                                     
 1518 .venv\Lib\site-packages\numpy\_core\tests\test_strings.py                         
 1518 .venv\Lib\site-packages\numpy\f2py\symbolic.py                                    
 1498 .venv\Lib\site-packages\numpy\typing\tests\data\pass\random.py                    
 1496 .venv\Lib\site-packages\pygame\tests\image_test.py                                
 1493 .venv\Lib\site-packages\urllib3\response.py                                       
 1487 .venv\Lib\site-packages\pip\_vendor\urllib3\response.py                           
 1467 .venv\Lib\site-packages\numpy\lib\_polynomial_impl.py                             
 1449 .venv\Lib\site-packages\numpy\lib\tests\test_nanfunctions.py                      
 1439 .venv\Lib\site-packages\pygame\tests\mixer_test.py                                
 1429 .venv\Lib\site-packages\numpy\_core\defchararray.py                               
 1427 .venv\Lib\site-packages\numpy\lib\tests\test_arraypad.py                          
 1409 .venv\Lib\site-packages\pip\_internal\cli\cmdoptions.py                           
 1406 .venv\Lib\site-packages\pygame\tests\sprite_test.py                               
 1403 .venv\Lib\site-packages\pip\_vendor\distro\distro.py                              
 1368 .venv\Lib\site-packages\numpy\_core\tests\test_einsum.py                          
 1363 .venv\Lib\site-packages\numpy\_core\tests\test_arrayprint.py                      
 1361 .venv\Lib\site-packages\pip\_vendor\rich\text.py                                  
 1355 ui\components\game_card.py                                                        
 1345 .venv\Lib\site-packages\numpy\_core\tests\test_simd.py                            
 1330 .venv\Lib\site-packages\PIL\ImageFont.py                                          
 1304 .venv\Lib\site-packages\numpy\lib\tests\test_arraysetops.py                       
 1247 .venv\Lib\site-packages\numpy\lib\_shape_base_impl.py                             
 1242 .venv\Lib\site-packages\numpy\lib\_twodim_base_impl.py                            
 1231 .venv\Lib\site-packages\pip\_vendor\packaging\version.py                          
 1223 .venv\Lib\site-packages\PIL\GifImagePlugin.py                                     
 1204 .venv\Lib\site-packages\pip\_vendor\pygments\lexers\python.py                     
 1191 .venv\Lib\site-packages\pip\_vendor\urllib3\connectionpool.py                     
 1191 .venv\Lib\site-packages\urllib3\connectionpool.py                                 
 1191 .venv\Lib\site-packages\numpy\polynomial\_polybase.py                             
 1184 .venv\Lib\site-packages\pygame\tests\font_test.py                                 
 1180 .venv\Lib\site-packages\pip\_vendor\requests\models.py                            
 1180 .venv\Lib\site-packages\requests\models.py                                        
 1167 .venv\Lib\site-packages\numpy\_core\tests\test_scalarmath.py                      
 1158 .venv\Lib\site-packages\numpy\lib\_arraysetops_impl.py                            
 1155 .venv\Lib\site-packages\pip\_vendor\requests\utils.py                             
 1155 .venv\Lib\site-packages\requests\utils.py                                         
 1152 .venv\Lib\site-packages\pip\_internal\index\package_finder.py                     
 1145 .venv\Lib\site-packages\pip\_internal\exceptions.py                               
 1117 .venv\Lib\site-packages\numpy\matrixlib\defmatrix.py                              
 1112 .venv\Lib\site-packages\pygame\tests\display_test.py                              
 1107 .venv\Lib\site-packages\pip\_vendor\distlib\compat.py                             
 1101 .venv\Lib\site-packages\numpy\_core\records.py                                    
 1099 .venv\Lib\site-packages\pip\_vendor\urllib3\connection.py                         
 1099 .venv\Lib\site-packages\urllib3\connection.py                                     
 1092 .venv\Lib\site-packages\PIL\PdfParser.py                                          
 1085 .venv\Lib\site-packages\numpy\lib\_histograms_impl.py                             
 1078 .venv\Lib\site-packages\PIL\ImageCms.py                                           
 1077 .venv\Lib\site-packages\numpy\lib\tests\test_loadtxt.py                           
 1063 .venv\Lib\site-packages\charset_normalizer\md.py                                  
 1048 .venv\Lib\site-packages\numpy\lib\_index_tricks_impl.py                           
 1043 .venv\Lib\site-packages\numpy\lib\tests\test_format.py                            
 1042 .venv\Lib\site-packages\numpy\lib\tests\test_recfunctions.py                      
 1038 .venv\Lib\site-packages\numpy\lib\_format_impl.py                                 
 1016 .venv\Lib\site-packages\pip\_vendor\rich\pretty.py                                
 1007 .venv\Lib\site-packages\pygame\tests\event_test.py                                
 1006 .venv\Lib\site-packages\pip\_vendor\rich\table.py                                 
 1006 .venv\Lib\site-packages\numpy\f2py\tests\test_f2py2e.py                           
 1005 .venv\Lib\site-packages\numpy\f2py\auxfuncs.py                                    
 1002 .venv\Lib\site-packages\PIL\ImageDraw.py                                          
  996 .venv\Lib\site-packages\numpy\_core\shape_base.py                                 
  986 .venv\Lib\site-packages\pygame\cursors.py                                         
  985 .venv\Lib\site-packages\pip\_vendor\rich\syntax.py                                
  970 .venv\Lib\site-packages\numpy\_core\tests\test_casting_unittests.py               
  965 .venv\Lib\site-packages\pip\_vendor\pygments\lexer.py                             
  964 .venv\Lib\site-packages\pip\_vendor\packaging\metadata.py                         
  964 .venv\Lib\site-packages\numpy\_core\_internal.py                                  
  943 .venv\Lib\site-packages\numpy\_core\tests\test_array_coercion.py                  
  942 .venv\Lib\site-packages\pip\_vendor\pygments\filters\__init__.py                  
  939 .venv\Lib\site-packages\numpy\ma\tests\test_old_ma.py                             
  939 .venv\Lib\site-packages\numpy\__init__.py                                         
  938 .venv\Lib\site-packages\PIL\ImageFile.py                                          
  934 .venv\Lib\site-packages\charset_normalizer\api.py                                 
  933 .venv\Lib\site-packages\numpy\_core\tests\test_mem_overlap.py                     
  932 .venv\Lib\site-packages\pip\_vendor\packaging\tags.py                             
  929 .venv\Lib\site-packages\pip\_vendor\msgpack\fallback.py                           
  926 .venv\Lib\site-packages\numpy\lib\_arraypad_impl.py                               
  920 .venv\Lib\site-packages\pip\_vendor\requests\sessions.py                          
  920 .venv\Lib\site-packages\requests\sessions.py                                      
  917 .venv\Lib\site-packages\pygame\tests\gfxdraw_test.py                              
  917 .venv\Lib\site-packages\pip\_vendor\platformdirs\__init__.py                      
  905 .venv\Lib\site-packages\pip\_vendor\packaging\pylock.py                           
  904 .venv\Lib\site-packages\pip\_internal\commands\install.py                         
  904 .venv\Lib\site-packages\numpy\_core\tests\test_shape_base.py                      
  901 .venv\Lib\site-packages\pip\_internal\resolution\resolvelib\factory.py            
  900 .venv\Lib\site-packages\numpy\lib\_iotools.py                                     
  899 .venv\Lib\site-packages\pip\_vendor\rich\traceback.py                             
  896 .venv\Lib\site-packages\pip\_internal\operations\prepare.py                       
  890 .venv\Lib\site-packages\numpy\lib\tests\test_stride_tricks.py                     
  889 .venv\Lib\site-packages\PIL\JpegImagePlugin.py                                    
  882 .venv\Lib\site-packages\numpy\random\tests\test_smoke.py                          
  879 .venv\Lib\site-packages\numpy\_core\tests\test_defchararray.py                    
  877 .venv\Lib\site-packages\pygame\examples\midi.py                                   
  862 .venv\Lib\site-packages\idna\core.py                                              
  855 .venv\Lib\site-packages\numpy\lib\tests\test_histograms.py                        
  842 .venv\Lib\site-packages\pip\_internal\req\req_install.py                          
  815 .venv\Lib\site-packages\pip\_internal\utils\misc.py                               
  813 .venv\Lib\site-packages\numpy\lib\tests\test_shape_base.py                        
  811 .venv\Lib\site-packages\numpy\f2py\capi_maps.py                                   
  800 .venv\Lib\site-packages\numpy\_core\tests\test_overrides.py                       
  799 .venv\Lib\site-packages\pip\_vendor\packaging\licenses\_spdx.py                   
  793 .venv\Lib\site-packages\pip\_vendor\tomli\_parser.py                              
  792 .venv\Lib\site-packages\pip\_vendor\rich\style.py                                 
  764 .venv\Lib\site-packages\pip\_internal\operations\install\wheel.py                 
  759 .venv\Lib\site-packages\numpy\polynomial\polyutils.py                             
  755 .venv\Lib\site-packages\numpy\f2py\f2py2e.py                                      
  752 .venv\Lib\site-packages\pip\_vendor\rich\segment.py                               
  750 .venv\Lib\site-packages\numpy\_core\tests\test_multithreading.py                  
  749 .venv\Lib\site-packages\PIL\ImageOps.py                                           
  748 .venv\Lib\site-packages\pip\_vendor\requests\adapters.py                          
  748 .venv\Lib\site-packages\requests\adapters.py                                      
  740 .venv\Lib\site-packages\PySide6\QtAsyncio\events.py                               
  739 .venv\Lib\site-packages\numpy\ma\mrecords.py                                      
  733 .venv\Lib\site-packages\pygame\tests\surfarray_test.py                            
  732 .venv\Lib\site-packages\numpy\f2py\tests\test_array_from_pyobj.py                 
  726 .venv\Lib\site-packages\pip\_vendor\urllib3\contrib\emscripten\fetch.py           
  726 .venv\Lib\site-packages\urllib3\contrib\emscripten\fetch.py                       
  723 .venv\Lib\site-packages\numpy\tests\test_public_api.py                            
  716 .venv\Lib\site-packages\pygame\midi.py                                            
  714 .venv\Lib\site-packages\numpy\lib\_type_check_impl.py                             
  713 .venv\Lib\site-packages\numpy\polynomial\tests\test_polynomial.py                 
  708 .venv\Lib\site-packages\pygame\tests\pixelcopy_test.py                            
  703 .venv\Lib\site-packages\numpy\lib\tests\test_index_tricks.py                      
  700 .venv\Lib\site-packages\numpy\lib\_datasource.py                                  
  694 .venv\Lib\site-packages\pip\_internal\vcs\versioncontrol.py                       
  692 .venv\Lib\site-packages\pygame\colordict.py                                       
  690 .venv\Lib\site-packages\pip\_internal\metadata\base.py                            
  668 .venv\Lib\site-packages\numpy\_core\tests\test_api.py                             
  662 .venv\Lib\site-packages\pip\_internal\req\constructors.py                         
  661 .venv\Lib\site-packages\pip\_vendor\rich\_win32_console.py                        
  657 .venv\Lib\site-packages\pip\_internal\models\link.py                              
  656 .venv\Lib\site-packages\numpy\lib\_stride_tricks_impl.py                          
  653 .venv\Lib\site-packages\pip\_vendor\urllib3\poolmanager.py                        
  653 .venv\Lib\site-packages\urllib3\poolmanager.py                                    
  649 .venv\Lib\site-packages\numpy\f2py\cb_rules.py                                    
  648 .venv\Lib\site-packages\pip\_vendor\idna\core.py                                  
  644 .venv\Lib\site-packages\pip\_internal\req\req_uninstall.py                        
  644 .venv\Lib\site-packages\numpy\f2py\tests\test_character.py                        
  642 .venv\Lib\site-packages\numpy\lib\_scimath_impl.py                                
  640 .venv\Lib\site-packages\numpy\_core\tests\test_numerictypes.py                    
  639 .venv\Lib\site-packages\numpy\polynomial\tests\test_chebyshev.py                  
  632 .venv\Lib\site-packages\PIL\DdsImagePlugin.py                                     
  631 .venv\Lib\site-packages\numpy\_core\tests\test_umath_complex.py                   
  627 .venv\Lib\site-packages\pip\_vendor\resolvelib\resolvers\resolution.py            
  625 .venv\Lib\site-packages\numpy\polynomial\tests\test_classes.py                    
  625 .venv\Lib\site-packages\pip\_vendor\requests\cookies.py                           
  625 .venv\Lib\site-packages\requests\cookies.py                                       
  622 .venv\Lib\site-packages\pip\_internal\req\req_file.py                             
  621 .venv\Lib\site-packages\pip\_vendor\rich\color.py                                 
  620 .venv\Lib\site-packages\numpy\random\tests\test_direct.py                         
  619 .venv\Lib\site-packages\pygame\tests\base_test.py                                 
  617 .venv\Lib\site-packages\PIL\ImageFilter.py                                        
  614 .venv\Lib\site-packages\numpy\typing\tests\data\pass\arithmetic.py                
  609 .venv\Lib\site-packages\numpy\fft\tests\test_pocketfft.py                         
  609 .venv\Lib\site-packages\numpy\_core\tests\test_records.py                         
  607 .venv\Lib\site-packages\pygame\examples\glcube.py                                 
  603 .venv\Lib\site-packages\numpy\ctypeslib\_ctypeslib.py                             
  603 .venv\Lib\site-packages\pip\_vendor\pygments\lexers\_mapping.py                   
  603 .venv\Lib\site-packages\pygame\tests\test_utils\buftools.py                       
  598 .venv\Lib\site-packages\pip\_internal\resolution\resolvelib\candidates.py         
  598 .venv\Lib\site-packages\pip\_internal\resolution\legacy\resolver.py               
  589 .venv\Lib\site-packages\numpy\_core\tests\test_half.py                            
  587 .venv\Lib\site-packages\numpy\polynomial\tests\test_legendre.py                   
  587 .venv\Lib\site-packages\pip\_internal\network\auth.py                             
  576 .venv\Lib\site-packages\numpy\_core\numerictypes.py                               
  575 .venv\Lib\site-packages\numpy\polynomial\tests\test_hermite_e.py                  
  574 .venv\Lib\site-packages\pip\_internal\vcs\git.py                                  
  574 .venv\Lib\site-packages\numpy\polynomial\tests\test_hermite.py                    
  571 .venv\Lib\site-packages\pip\_vendor\truststore\_macos.py                          
  569 .venv\Lib\site-packages\pygame\sysfont.py                                         
  567 .venv\Lib\site-packages\pip\_vendor\truststore\_windows.py                        
  566 .venv\Lib\site-packages\PIL\TiffTags.py                                           
  564 .venv\Lib\site-packages\numpy\lib\tests\test_twodim_base.py                       
  563 .venv\Lib\site-packages\pip\_vendor\urllib3\contrib\pyopenssl.py                  
  563 .venv\Lib\site-packages\urllib3\contrib\pyopenssl.py                              
  562 .venv\Lib\site-packages\numpy\polynomial\tests\test_printing.py                   
  557 .venv\Lib\site-packages\urllib3\util\retry.py                                     
  557 .venv\Lib\site-packages\pip\_vendor\urllib3\util\retry.py                         
  557 ui\main_window_history.py                                                         
  556 .venv\Lib\site-packages\numpy\polynomial\tests\test_laguerre.py                   
  547 .venv\Lib\site-packages\numpy\_core\function_base.py                              
  541 .venv\Lib\site-packages\numpy\lib\_utils_impl.py                                  
  533 .venv\Lib\site-packages\numpy\_core\tests\test_cpu_features.py                    
  532 .venv\Lib\site-packages\pip\_internal\network\session.py                          
  531 .venv\Lib\site-packages\pygame\tests\mixer_music_test.py                          
  526 .venv\Lib\site-packages\PySide6\scripts\deploy_lib\config.py                      
  515 .venv\Lib\site-packages\numpy\_core\_ufunc_config.py                              
  514 .venv\Lib\site-packages\PIL\BmpImagePlugin.py                                     
  511 .venv\Lib\site-packages\numpy\_core\tests\test_custom_dtypes.py                   
  511 .venv\Lib\site-packages\numpy\_core\tests\test_deprecations.py                    
  511 .venv\Lib\site-packages\pygame\tests\time_test.py                                 
  511 .venv\Lib\site-packages\pip\_vendor\cachecontrol\controller.py                    
  510 .venv\Lib\site-packages\pip\_internal\index\collector.py                          
  509 .venv\Lib\site-packages\PIL\ImageText.py                                          
  508 .venv\Lib\site-packages\PySide6\scripts\metaobjectdump.py                         
  504 .venv\Lib\site-packages\pip\_internal\cli\req_command.py                          
  502 .venv\Lib\site-packages\numpy\_core\tests\test_function_base.py                   
  502 .venv\Lib\site-packages\pygame\tests\bufferproxy_test.py                          
  501 .venv\Lib\site-packages\numpy\f2py\tests\test_symbolic.py                         
  498 .venv\Lib\site-packages\PIL\BlpImagePlugin.py                                     
  495 .venv\Lib\site-packages\numpy\ma\tests\test_mrecords.py                           
  492 .venv\Lib\site-packages\pip\_vendor\packaging\markers.py                          
  490 .venv\Lib\site-packages\pygame\tests\render_test.py                               
  486 .venv\Lib\site-packages\urllib3\_collections.py                                   
  486 .venv\Lib\site-packages\pip\_vendor\urllib3\_collections.py                       
  486 .venv\Lib\site-packages\numpy\_utils\_pep440.py                                   
  484 .venv\Lib\site-packages\PIL\EpsImagePlugin.py                                     
  482 .venv\Lib\site-packages\pip\_vendor\rich\_spinners.py                             
  478 ui\main_window_games.py                                                           
  477 .venv\Lib\site-packages\pip\_vendor\urllib3\util\ssl_.py                          
  477 .venv\Lib\site-packages\urllib3\util\ssl_.py                                      
  475 .venv\Lib\site-packages\numpy\matrixlib\tests\test_defmatrix.py                   
  474 .venv\Lib\site-packages\pip\_vendor\rich\box.py                                   
  474 .venv\Lib\site-packages\pygame\__init__.py                                        
  473 .venv\Lib\site-packages\numpy\lib\tests\test_type_check.py                        
  469 .venv\Lib\site-packages\pip\_vendor\urllib3\util\url.py                           
  469 .venv\Lib\site-packages\numpy\ma\tests\test_subclassing.py                        
  469 .venv\Lib\site-packages\urllib3\util\url.py                                       
  467 .venv\Lib\site-packages\charset_normalizer\cd.py                                  
  466 .venv\Lib\site-packages\PIL\Jpeg2KImagePlugin.py                                  
  463 .venv\Lib\site-packages\pip\_vendor\platformdirs\api.py                           
  462 .venv\Lib\site-packages\pygame\tests\midi_test.py                                 
  461 .venv\Lib\site-packages\pygame\tests\window_test.py                               
  457 .venv\Lib\site-packages\pygame\surfarray.py                                       
  454 .venv\Lib\site-packages\pip\_vendor\rich\_cell_widths.py                          
  452 .venv\Lib\site-packages\charset_normalizer\utils.py                               
  451 .venv\Lib\site-packages\pip\_vendor\distlib\scripts.py                            
  449 .venv\Lib\site-packages\numpy\_core\getlimits.py                                  
  448 .venv\Lib\site-packages\numpy\_core\tests\test_mem_policy.py                      
  443 .venv\Lib\site-packages\PySide6\scripts\qtpy2cpp_lib\visitor.py                   
  442 .venv\Lib\site-packages\pip\_vendor\rich\layout.py                                
  442 .venv\Lib\site-packages\numpy\f2py\tests\util.py                                  
  438 .venv\Lib\site-packages\pygame\tests\test_utils\arrinter.py                       
  438 .venv\Lib\site-packages\pip\_internal\locations\__init__.py                       
  427 .venv\Lib\site-packages\numpy\f2py\tests\test_crackfortran.py                     
  426 .venv\Lib\site-packages\pygame\tests\constants_test.py                            
  420 .venv\Lib\site-packages\pygame\tests\mouse_test.py                                
  410 .venv\Lib\site-packages\pip\_vendor\pyproject_hooks\_impl.py                      
  408 .venv\Lib\site-packages\pip\_internal\commands\list.py                            
  407 .venv\Lib\site-packages\pip\_internal\utils\unpacking.py                          
  406 .venv\Lib\site-packages\numpy\_core\tests\test_cython.py                          
  406 .venv\Lib\site-packages\numpy\tests\test_ctypeslib.py                             
  404 .venv\Lib\site-packages\pip\_internal\utils\logging.py                            
  403 .venv\Lib\site-packages\numpy\_core\tests\test_scalarprint.py                     
  401 .venv\Lib\site-packages\PIL\IcnsImagePlugin.py                                    
  400 .venv\Lib\site-packages\pip\_vendor\rich\live.py                                  
  400 .venv\Lib\site-packages\pip\_vendor\rich\prompt.py                                
  400 .venv\Lib\site-packages\pygame\examples\aliens.py                                 
  396 .venv\Lib\site-packages\PIL\IcoImagePlugin.py                                     
  395 .venv\Lib\site-packages\pip\_vendor\platformdirs\windows.py                       
  395 .venv\Lib\site-packages\pip\_internal\configuration.py                            
  393 .venv\Lib\site-packages\pip\_vendor\packaging\_parser.py                          
  390 .venv\Lib\site-packages\PIL\ImImagePlugin.py                                      
  389 .venv\Lib\site-packages\pip\_vendor\pyproject_hooks\_in_process\_in_process.py    
  387 .venv\Lib\site-packages\charset_normalizer\models.py                              
  387 .venv\Lib\site-packages\pip\_internal\network\download.py                         
  384 .venv\Lib\site-packages\PIL\ExifTags.py                                           
  383 ui\main_window_theme.py                                                           
  381 .venv\Lib\site-packages\numpy\_core\_add_newdocs_scalars.py                       
  380 .venv\Lib\site-packages\numpy\matlib.py                                           
  378 main.py                                                                           
  377 .venv\Lib\site-packages\PySide6\scripts\project.py                                
  375 .venv\Lib\site-packages\PIL\PpmImagePlugin.py                                     
  374 .venv\Lib\site-packages\numpy\lib\tests\test_packbits.py                          
  372 .venv\Lib\site-packages\pip\_vendor\distlib\resources.py                          
  370 .venv\Lib\site-packages\numpy\_core\tests\test_longdouble.py                      
  369 .venv\Lib\site-packages\numpy\_core\tests\test_unicode.py                         
  367 .venv\Lib\site-packages\PIL\ImageShow.py                                          
  366 .venv\Lib\site-packages\pip\_internal\cli\parser.py                               
  366 .venv\Lib\site-packages\numpy\_core\_dtype.py                                     
  365 .venv\Lib\site-packages\numpy\_core\tests\test_scalar_methods.py                  
  363 .venv\Lib\site-packages\charset_normalizer\cli\__main__.py                        
  362 .venv\Lib\site-packages\pip\_vendor\pygments\lexers\__init__.py                   
  362 .venv\Lib\site-packages\numpy\_core\memmap.py                                     
  360 .venv\Lib\site-packages\numpy\matrixlib\tests\test_interaction.py                 
  358 .venv\Lib\site-packages\numpy\lib\tests\test__iotools.py                          
  356 .venv\Lib\site-packages\pip\_vendor\urllib3\http2\connection.py                   
  356 .venv\Lib\site-packages\urllib3\http2\connection.py                               
  354 .venv\Lib\site-packages\pip\_vendor\requests\auth.py                              
  354 .venv\Lib\site-packages\requests\auth.py                                          
  349 .venv\Lib\site-packages\numpy\_array_api_info.py                                  
  343 .venv\Lib\site-packages\pygame\tests\test_utils\run_tests.py                      
  343 .venv\Lib\site-packages\PIL\features.py                                           
  341 .venv\Lib\site-packages\pip\_internal\resolution\resolvelib\resolver.py           
  341 .venv\Lib\site-packages\pip\_vendor\truststore\_api.py                            
  341 .venv\Lib\site-packages\urllib3\fields.py                                         
  341 .venv\Lib\site-packages\pip\_vendor\urllib3\fields.py                             
  339 core\tray.py                                                                      
  339 .venv\Lib\site-packages\PIL\PsdImagePlugin.py                                     
  335 .venv\Lib\site-packages\pip\_internal\vcs\subversion.py                           
  335 .venv\Lib\site-packages\pip\_vendor\urllib3\exceptions.py                         
  335 .venv\Lib\site-packages\urllib3\exceptions.py                                     
  334 .venv\Lib\site-packages\PySide6\scripts\deploy_lib\dependency_util.py             
  333 .venv\Lib\site-packages\pip\_internal\build_env\installer.py                      
  333 .venv\Lib\site-packages\numpy\lib\tests\test_polynomial.py                        
  332 .venv\Lib\site-packages\PIL\SpiderImagePlugin.py                                  
  330 .venv\Lib\site-packages\pygame\tests\test_utils\test_runner.py                    
  330 core\scrapers\store_scrapers.py                                                   
  329 .venv\Lib\site-packages\numpy\f2py\func2subr.py                                   
  328 .venv\Lib\site-packages\numpy\lib\tests\test__datasource.py                       
  325 .venv\Lib\site-packages\pip\_vendor\packaging\direct_url.py                       
  324 .venv\Lib\site-packages\pip\_vendor\pygments\util.py                              
  322 .venv\Lib\site-packages\PIL\WebPImagePlugin.py                                    
  322 ui\main_window_ui.py                                                              
  321 .venv\Lib\site-packages\pip\_vendor\platformdirs\unix.py                          
  320 .venv\Lib\site-packages\PIL\ImageColor.py                                         
  319 .venv\Lib\site-packages\pygame\tests\key_test.py                                  
  317 .venv\Lib\site-packages\PIL\ImageMorph.py                                         
  317 .venv\Lib\site-packages\pip\_vendor\rich\panel.py                                 
  316 .venv\Lib\site-packages\numpy\typing\tests\data\pass\comparisons.py               
  315 .venv\Lib\site-packages\PIL\PdfImagePlugin.py                                     
  314 .venv\Lib\site-packages\PIL\ImageMath.py                                          
  314 .venv\Lib\site-packages\pygame\examples\textinput.py                              
  311 .venv\Lib\site-packages\PIL\ImageChops.py                                         
  311 .venv\Lib\site-packages\PySide6\scripts\pyside_tool.py                            
  310 .venv\Lib\site-packages\numpy\lib\_user_array_impl.py                             
  309 .venv\Lib\site-packages\pip\_internal\resolution\resolvelib\provider.py           
  309 .venv\Lib\site-packages\pip\_vendor\rich\_palettes.py                             
  306 .venv\Lib\site-packages\pip\_vendor\rich\align.py                                 
  302 .venv\Lib\site-packages\pip\_vendor\packaging\dependency_groups.py                
  301 .venv\Lib\site-packages\pygame\tests\test_utils\async_sub.py                      
  300 .venv\Lib\site-packages\pip\_vendor\platformdirs\android.py                       
  299 .venv\Lib\site-packages\pip\_internal\utils\pylock.py                             
  298 .venv\Lib\site-packages\pip\_internal\metadata\pkg_resources.py                   
  297 .venv\Lib\site-packages\pip\_vendor\rich\logging.py                               
  296 .venv\Lib\site-packages\pip\_vendor\packaging\utils.py                            
  295 .venv\Lib\site-packages\PIL\AvifImagePlugin.py                                    
  294 .venv\Lib\site-packages\pip\_internal\cache.py                                    
  294 .venv\Lib\site-packages\numpy\ma\testutils.py                                     
  294 .venv\Lib\site-packages\pygame\tests\cursors_test.py                              
  293 .venv\Lib\site-packages\pip\_internal\utils\temp_dir.py                           
  290 .venv\Lib\site-packages\PIL\ImagePalette.py                                       
  289 .venv\Lib\site-packages\pip\_internal\commands\configuration.py                   
  287 .venv\Lib\site-packages\numpy\_core\tests\test_nep50_promotions.py                
  286 .venv\Lib\site-packages\pygame\examples\font_viewer.py                            
  286 .venv\Lib\site-packages\pip\_internal\index\sources.py                            
  286 .venv\Lib\site-packages\numpy\_core\tests\test_memmap.py                          
  284 .venv\Lib\site-packages\PIL\TgaImagePlugin.py                                     
  281 .venv\Lib\site-packages\numpy\f2py\f90mod_rules.py                                
  281 .venv\Lib\site-packages\urllib3\contrib\emscripten\response.py                    
  281 .venv\Lib\site-packages\pip\_vendor\urllib3\contrib\emscripten\response.py        
  278 .venv\Lib\site-packages\pip\_vendor\urllib3\_request_methods.py                   
  278 .venv\Lib\site-packages\urllib3\_request_methods.py                               
  275 .venv\Lib\site-packages\urllib3\util\timeout.py                                   
  275 .venv\Lib\site-packages\pip\_vendor\urllib3\util\timeout.py                       
  272 .venv\Lib\site-packages\numpy\typing\tests\data\pass\fromnumeric.py               
  271 .venv\Lib\site-packages\pygame\tests\controller_test.py                           
  271 .venv\Lib\site-packages\pip\_vendor\urllib3\util\ssltransport.py                  
  271 .venv\Lib\site-packages\urllib3\util\ssltransport.py                              
  269 .venv\Lib\site-packages\PySide6\scripts\project_lib\project_data.py               
  268 .venv\Lib\site-packages\pip\_vendor\rich\_inspect.py                              
  266 .venv\Lib\site-packages\PySide6\scripts\qtpy2cpp_lib\formatter.py                 
  266 .venv\Lib\site-packages\PIL\ImageTk.py                                            
  265 .venv\Lib\site-packages\pip\_internal\wheel_builder.py                            
  263 .venv\Lib\site-packages\urllib3\util\request.py                                   
  262 .venv\Lib\site-packages\numpy\typing\tests\data\pass\scalars.py                   
  262 .venv\Lib\site-packages\numpy\_core\tests\test_dlpack.py                          
  262 .venv\Lib\site-packages\PIL\FpxImagePlugin.py                                     
  262 .venv\Lib\site-packages\pip\_vendor\packaging\_manylinux.py                       
  262 .venv\Lib\site-packages\numpy\f2py\tests\test_callback.py                         
  261 .venv\Lib\site-packages\numpy\_core\tests\test_limited_api.py                     
  261 .venv\Lib\site-packages\pip\_internal\cli\base_command.py                         
  260 .venv\Lib\site-packages\urllib3\contrib\emscripten\connection.py                  
  260 .venv\Lib\site-packages\pip\_vendor\urllib3\contrib\emscripten\connection.py      
  259 .venv\Lib\site-packages\pip\_internal\operations\freeze.py                        
  257 .venv\Lib\site-packages\pip\_vendor\rich\tree.py                                  
  256 .venv\Lib\site-packages\pygame\examples\cursors.py                                
  256 .venv\Lib\site-packages\PIL\PcfFontFile.py                                        
  256 .venv\Lib\site-packages\pip\_internal\commands\cache.py                           
  254 .venv\Lib\site-packages\pip\_vendor\urllib3\util\request.py                       
  253 .venv\Lib\site-packages\pygame\tests\blit_test.py                                 
  252 .venv\Lib\site-packages\numpy\_core\_methods.py                                   
  251 .venv\Lib\site-packages\pip\_internal\resolution\resolvelib\requirements.py       
  251 .venv\Lib\site-packages\pip\_vendor\rich\markup.py                                
  249 .venv\Lib\site-packages\numpy\conftest.py                                         
  249 .venv\Lib\site-packages\pip\_internal\utils\subprocess.py                         
  249 .venv\Lib\site-packages\numpy\random\tests\test_randomstate_regression.py         
  248 .venv\Lib\site-packages\PySide6\scripts\qml.py                                    
  247 .venv\Lib\site-packages\numpy\testing\_private\extbuild.py                        
  247 .venv\Lib\site-packages\PIL\ImageWin.py                                           
  247 .venv\Lib\site-packages\pip\_vendor\pygments\sphinxext.py                         
  247 .venv\Lib\site-packages\numpy\f2py\_src_pyf.py                                    
  246 .venv\Lib\site-packages\numpy\exceptions.py                                       
  246 ui\main_window_helpers.py                                                         
  246 .venv\Lib\site-packages\pip\_internal\self_outdated_check.py                      
  245 .venv\Lib\site-packages\pip\_vendor\rich\__main__.py                              
  244 .venv\Lib\site-packages\PySide6\scripts\project_lib\pyproject_toml.py             
  244 .venv\Lib\site-packages\PIL\ImageDraw2.py                                         
  244 .venv\Lib\site-packages\numpy\f2py\_backends\_meson.py                            
  242 .venv\Lib\site-packages\pygame\examples\music_drop_fade.py                        
  242 .venv\Lib\site-packages\PIL\JpegPresets.py                                        
  241 .venv\Lib\site-packages\pip\_vendor\rich\ansi.py                                  
  240 .venv\Lib\site-packages\numpy\matrixlib\tests\test_masked_matrix.py               
  240 .venv\Lib\site-packages\numpy\random\tests\test_generator_mt19937_regressions.py  
  238 .venv\Lib\site-packages\PIL\PSDraw.py                                             
  237 .venv\Lib\site-packages\pip\_internal\commands\show.py                            
  237 .venv\Lib\site-packages\pygame\examples\testsprite.py                             
  235 .venv\Lib\site-packages\PIL\QoiImagePlugin.py                                     
  235 .venv\Lib\site-packages\numpy\fft\_helper.py                                      
  235 .venv\Lib\site-packages\pip\_internal\cli\spinners.py                             
  235 .venv\Lib\site-packages\pip\_internal\metadata\importlib\_dists.py                
  234 .venv\Lib\site-packages\PIL\ImageGrab.py                                          
  232 .venv\Lib\site-packages\pip\_vendor\rich\highlighter.py                           
  232 .venv\Lib\site-packages\PIL\PcxImagePlugin.py                                     
  232 .venv\Lib\site-packages\pygame\ftfont.py                                          
  231 .venv\Lib\site-packages\PIL\SgiImagePlugin.py                                     
  231 .venv\Lib\site-packages\numpy\lib\tests\test_regression.py                        
  229 .venv\Lib\site-packages\pip\_vendor\tomli_w\_writer.py                            
  228 .venv\Lib\site-packages\urllib3\contrib\socks.py                                  
  228 .venv\Lib\site-packages\pip\_vendor\urllib3\contrib\socks.py                      
  226 .venv\Lib\site-packages\PIL\IptcImagePlugin.py                                    
  225 .venv\Lib\site-packages\numpy\typing\__init__.py                                  
  224 .venv\Lib\site-packages\numpy\lib\_arrayterator_impl.py                           
  224 ui\modals\settings_modal.py                                                       
  223 .venv\Lib\site-packages\pip\_vendor\platformdirs\macos.py                         
  223 .venv\Lib\site-packages\pip\_vendor\rich\progress_bar.py                          
  222 .venv\Lib\site-packages\numpy\_core\tests\test_array_interface.py                 
  221 .venv\Lib\site-packages\pygame\tests\scrap_test.py                                
  219 .venv\Lib\site-packages\PIL\ImageQt.py                                            
  219 .venv\Lib\site-packages\requests\__init__.py                                      
  219 .venv\Lib\site-packages\pip\_vendor\rich\control.py                               
  218 .venv\Lib\site-packages\pip\_internal\locations\_sysconfig.py                     
  218 .venv\Lib\site-packages\pygame\examples\sound_array_demos.py                      
  217 .venv\Lib\site-packages\PySide6\QtAsyncio\tasks.py                                
  217 .venv\Lib\site-packages\PIL\PalmImagePlugin.py                                    
  217 .venv\Lib\site-packages\numpy\_core\tests\test_extint128.py                       
  217 .venv\Lib\site-packages\pip\_internal\cli\index_command.py                        
  217 .venv\Lib\site-packages\numpy\polynomial\tests\test_symbol.py                     
  217 logger.py                                                                         
  215 .venv\Lib\site-packages\numpy\lib\tests\test_mixins.py                            
  215 .venv\Lib\site-packages\pip\_internal\network\lazy_wheel.py                       
  214 .venv\Lib\site-packages\pip\_vendor\requests\__init__.py                          
  214 .venv\Lib\site-packages\pip\_vendor\pygments\token.py                             
  213 .venv\Lib\site-packages\numpy\fft\__init__.py                                     
  213 .venv\Lib\site-packages\numpy\random\__init__.py                                  
  212 .venv\Lib\site-packages\numpy\lib\_ufunclike_impl.py                              
  211 .venv\Lib\site-packages\urllib3\__init__.py                                       
  211 .venv\Lib\site-packages\pip\_vendor\urllib3\__init__.py                           
  209 .venv\Lib\site-packages\numpy\_core\tests\test_conversion_utils.py                
  209 .venv\Lib\site-packages\pip\_vendor\resolvelib\structs.py                         
  207 .venv\Lib\site-packages\numpy\typing\tests\test_typing.py                         
  207 .venv\Lib\site-packages\numpy\testing\print_coercion_tables.py                    
  206 .venv\Lib\site-packages\pip\_internal\network\utils.py                            
  203 .venv\Lib\site-packages\numpy\_core\tests\test_scalar_ctors.py                    
  203 .venv\Lib\site-packages\pip\_vendor\pygments\style.py                             
  203 .venv\Lib\site-packages\PIL\MpoImagePlugin.py                                     
  203 .venv\Lib\site-packages\pygame\examples\blit_blends.py                            
  203 .venv\Lib\site-packages\numpy\_core\__init__.py                                   
  202 .venv\Lib\site-packages\numpy\f2py\tests\test_regression.py                       
  202 .venv\Lib\site-packages\numpy\_core\tests\test_print.py                           
  202 .venv\Lib\site-packages\pygame\examples\mask.py                                   
  201 .venv\Lib\site-packages\pip\_internal\utils\filesystem.py                         
  201 .venv\Lib\site-packages\pip\_internal\utils\compatibility_tags.py                 
  200 .venv\Lib\site-packages\pygame\examples\chimp.py                                  
  200 .venv\Lib\site-packages\numpy\typing\mypy_plugin.py                               
  200 .venv\Lib\site-packages\PIL\MspImagePlugin.py                                     
  199 .venv\Lib\site-packages\numpy\typing\tests\data\pass\ma.py                        
  199 .venv\Lib\site-packages\numpy\typing\tests\data\pass\ndarray_misc.py              
  198 .venv\Lib\site-packages\numpy\_core\tests\test_arrayobject.py                     
  198 .venv\Lib\site-packages\pygame\examples\scroll.py                                 
  196 .venv\Lib\site-packages\pip\_vendor\resolvelib\providers.py                       
  195 .venv\Lib\site-packages\pip\_internal\commands\debug.py                           
  194 ui\components\notification_toast.py                                               
  194 .venv\Lib\site-packages\PySide6\scripts\project_lib\utils.py                      
  193 .venv\Lib\site-packages\pip\_vendor\rich\default_styles.py                        
  193 core\i18n.py                                                                      
  193 .venv\Lib\site-packages\pip\_internal\distributions\sdist.py                      
  193 .venv\Lib\site-packages\pip\_vendor\packaging\_tokenizer.py                       
  192 .venv\Lib\site-packages\numpy\_utils\_inspect.py                                  
  191 .venv\Lib\site-packages\numpy\linalg\tests\test_regression.py                     
  189 .venv\Lib\site-packages\PySide6\scripts\project_lib\newproject.py                 
  188 .venv\Lib\site-packages\numpy\_core\overrides.py                                  
  188 .venv\Lib\site-packages\numpy\_core\tests\test_getlimits.py                       
  187 .venv\Lib\site-packages\pip\_internal\cli\autocompletion.py                       
  187 .venv\Lib\site-packages\numpy\polynomial\__init__.py                              
  187 .venv\Lib\site-packages\pip\_vendor\rich\columns.py                               
  186 .venv\Lib\site-packages\numpy\_pytesttester.py                                    
  186 .venv\Lib\site-packages\pip\_vendor\packaging\licenses\__init__.py                
  186 .venv\Lib\site-packages\pygame\_debug.py                                          
  186 .venv\Lib\site-packages\pip\_internal\vcs\mercurial.py                            
  184 .venv\Lib\site-packages\PIL\FliImagePlugin.py                                     
  184 .venv\Lib\site-packages\pygame\camera.py                                          
  183 .venv\Lib\site-packages\pygame\examples\eventlist.py                              
  183 .venv\Lib\site-packages\requests\_types.py                                        
  183 .venv\Lib\site-packages\pip\_vendor\requests\_types.py                            
  183 .venv\Lib\site-packages\PIL\WmfImagePlugin.py                                     
  180 .venv\Lib\site-packages\numpy\lib\mixins.py                                       
  180 .venv\Lib\site-packages\pip\_vendor\requests\api.py                               
  180 ui\main_window_navigation.py                                                      
  180 .venv\Lib\site-packages\PySide6\scripts\deploy_lib\nuitka_helper.py               
  180 .venv\Lib\site-packages\pygame\tests\test_utils\__init__.py                       
  180 .venv\Lib\site-packages\requests\api.py                                           
  178 .venv\Lib\site-packages\numpy\_core\tests\test_item_selection.py                  
  178 .venv\Lib\site-packages\pip\_internal\commands\search.py                          
  177 .venv\Lib\site-packages\pip\_internal\commands\wheel.py                           
  177 .venv\Lib\site-packages\pip\_vendor\rich\__init__.py                              
  175 .venv\Lib\site-packages\PySide6\scripts\deploy.py                                 
  175 .venv\Lib\site-packages\pygame\_camera_opencv.py                                  
  174 .venv\Lib\site-packages\numpy\random\tests\test_regression.py                     
  174 .venv\Lib\site-packages\pip\_internal\operations\check.py                         
  174 .venv\Lib\site-packages\pip\_vendor\rich\cells.py                                 
  173 .venv\Lib\site-packages\pip\_internal\locations\_distutils.py                     
  173 .venv\Lib\site-packages\pip\_internal\commands\index.py                           
  173 .venv\Lib\site-packages\PIL\ContainerIO.py                                        
  173 .venv\Lib\site-packages\pip\_internal\commands\lock.py                            
  171 .venv\Lib\site-packages\pip\_vendor\platformdirs\_xdg.py                          
  171 core\translator.py                                                                
  170 .venv\Lib\site-packages\numpy\typing\tests\data\pass\simple.py                    
  170 .venv\Lib\site-packages\pygame\tests\joystick_test.py                             
  170 .venv\Lib\site-packages\numpy\__config__.py                                       
  170 .venv\Lib\site-packages\pip\_vendor\msgpack\ext.py                                
  169 .venv\Lib\site-packages\pip\_internal\metadata\__init__.py                        
  167 .venv\Lib\site-packages\pip\_vendor\urllib3\_base_connection.py                   
  167 .venv\Lib\site-packages\numpy\fft\tests\test_helper.py                            
  167 .venv\Lib\site-packages\pip\_vendor\cachecontrol\adapter.py                       
  167 .venv\Lib\site-packages\pip\_vendor\rich\containers.py                            
  167 .venv\Lib\site-packages\PIL\ImageStat.py                                          
  167 .venv\Lib\site-packages\urllib3\_base_connection.py                               
  166 .venv\Lib\site-packages\pip\_internal\resolution\resolvelib\found_candidates.py   
  164 .venv\Lib\site-packages\pip\_internal\resolution\resolvelib\base.py               
  164 .venv\Lib\site-packages\numpy\typing\tests\data\pass\recfunctions.py              
  164 .venv\Lib\site-packages\pygame\examples\ninepatch.py                              
  163 .venv\Lib\site-packages\pygame\examples\video.py                                  
  163 .venv\Lib\site-packages\idna\codec.py                                             
  163 .venv\Lib\site-packages\pygame\examples\freetype_misc.py                          
  162 .venv\Lib\site-packages\numpy\_core\_exceptions.py                                
  162 .venv\Lib\site-packages\requests\exceptions.py                                    
  162 .venv\Lib\site-packages\pip\_vendor\requests\exceptions.py                        
  160 ui\components\store_widget.py                                                     
  160 .venv\Lib\site-packages\PIL\FontFile.py                                           
  159 .venv\Lib\site-packages\pip\_vendor\idna\codec.py                                 
  159 core\steam_enricher.py                                                            
  157 .venv\Lib\site-packages\PIL\XpmImagePlugin.py                                     
  157 .venv\Lib\site-packages\pip\_vendor\cachecontrol\heuristics.py                    
  157 .venv\Lib\site-packages\pip\_vendor\pygments\formatters\__init__.py               
  157 .venv\Lib\site-packages\pygame\examples\multiplayer_joystick.py                   
  156 .venv\Lib\site-packages\numpy\_core\tests\test_hashtable.py                       
  156 .venv\Lib\site-packages\numpy\_typing\_char_codes.py                              
  154 .venv\Lib\site-packages\numpy\_core\tests\test_scalarbuffer.py                    
  154 .venv\Lib\site-packages\PIL\GimpGradientFile.py                                   
  154 .venv\Lib\site-packages\numpy\_core\tests\test_casting_floatingpoint_errors.py    
  153 .venv\Lib\site-packages\numpy\lib\_version.py                                     
  153 .venv\Lib\site-packages\pip\_vendor\urllib3\util\ssl_match_hostname.py            
  153 .venv\Lib\site-packages\urllib3\util\ssl_match_hostname.py                        
  153 .venv\Lib\site-packages\numpy\_typing\_add_docstring.py                           
  153 .venv\Lib\site-packages\PIL\FitsImagePlugin.py                                    
  153 .venv\Lib\site-packages\pygame\tests\sndarray_test.py                             
  153 .venv\Lib\site-packages\pip\_internal\cli\progress_bars.py                        
  153 .venv\Lib\site-packages\pip\_vendor\pygments\unistring.py                         
  153 .venv\Lib\site-packages\pip\_vendor\rich\terminal_theme.py                        
  153 .venv\Lib\site-packages\pip\_vendor\rich\_ratio.py                                
  151 .venv\Lib\site-packages\pip\_vendor\rich\measure.py                               
  150 .venv\Lib\site-packages\pip\_internal\utils\hashes.py                             
  150 tests\test_history.py                                                             
  150 .venv\Lib\site-packages\pip\_internal\commands\download.py                        
  149 .venv\Lib\site-packages\numpy\typing\tests\data\pass\mod.py                       
  149 .venv\Lib\site-packages\pip\_vendor\rich\repr.py                                  
  148 .venv\Lib\site-packages\pip\_internal\metadata\importlib\_envs.py                 
  148 .venv\Lib\site-packages\pygame\__briefcase\pygame_ce.py                           
  147 .venv\Lib\site-packages\pygame\examples\scaletest.py                              
  147 .venv\Lib\site-packages\numpy\_typing\__init__.py                                 
  146 .venv\Lib\site-packages\PySide6\scripts\deploy_lib\__init__.py                    
  146 .venv\Lib\site-packages\pip\_vendor\cachecontrol\serialize.py                     
  145 .venv\Lib\site-packages\numpy\f2py\common_rules.py                                
  145 .venv\Lib\site-packages\pip\_internal\build_env\venv.py                           
  145 .venv\Lib\site-packages\PIL\SunImagePlugin.py                                     
  145 .venv\Lib\site-packages\pip\_vendor\cachecontrol\caches\file_cache.py             
  144 .venv\Lib\site-packages\pygame\tests\surflock_test.py                             
  144 .venv\Lib\site-packages\numpy\_core\tests\_natype.py                              
  144 .venv\Lib\site-packages\pip\_internal\utils\deprecation.py                        
  144 .venv\Lib\site-packages\PySide6\__init__.py                                       
  143 .venv\Lib\site-packages\pygame\examples\pixelarray.py                             
  143 .venv\Lib\site-packages\pygame\tests\__main__.py                                  
  141 .venv\Lib\site-packages\pip\_vendor\rich\padding.py                               
  141 .venv\Lib\site-packages\PySide6\scripts\deploy_lib\python_helper.py               
  141 .venv\Lib\site-packages\pygame\examples\joystick.py                               
  140 .venv\Lib\site-packages\pip\_internal\operations\build\build_tracker.py           
  139 .venv\Lib\site-packages\pip\_internal\build_env\virtual.py                        
  139 .venv\Lib\site-packages\pip\_vendor\rich\json.py                                  
  139 .venv\Lib\site-packages\pip\_internal\commands\__init__.py                        
  138 .venv\Lib\site-packages\numpy\doc\ufuncs.py                                       
  138 .venv\Lib\site-packages\pygame\sndarray.py                                        
  137 .venv\Lib\site-packages\numpy\typing\tests\data\pass\array_constructors.py        
  137 .venv\Lib\site-packages\urllib3\util\connection.py                                
  137 .venv\Lib\site-packages\pip\_vendor\urllib3\util\connection.py                    
  136 .venv\Lib\site-packages\PIL\ImageTransform.py                                     
  136 .venv\Lib\site-packages\pip\_internal\commands\completion.py                      
  135 .venv\Lib\site-packages\pygame\examples\stars.py                                  
  135 .venv\Lib\site-packages\pip\_internal\cli\main_parser.py                          
  134 .venv\Lib\site-packages\pygame\tests\rwobject_test.py                             
  134 .venv\Lib\site-packages\requests\help.py                                          
  132 .venv\Lib\site-packages\idna\cli.py                                               
  132 .venv\Lib\site-packages\pip\_vendor\rich\spinner.py                               
  132 .venv\Lib\site-packages\pip\_internal\utils\wheel.py                              
  131 .venv\Lib\site-packages\pygame\examples\playmus.py                                
  131 .venv\Lib\site-packages\numpy\typing\tests\data\pass\bitwise_ops.py               
  131 .venv\Lib\site-packages\pip\_vendor\rich\status.py                                
  131 .venv\Lib\site-packages\numpy\_core\tests\test_errstate.py                        
  130 .venv\Lib\site-packages\numpy\_core\_type_aliases.py                              
  130 .venv\Lib\site-packages\numpy\_core\_asarray.py                                   
  130 .venv\Lib\site-packages\requests\structures.py                                    
  130 .venv\Lib\site-packages\pip\_vendor\rich\rule.py                                  
  130 .venv\Lib\site-packages\pip\_internal\vcs\bazaar.py                               
  130 .venv\Lib\site-packages\pip\_vendor\requests\structures.py                        
  129 .venv\Lib\site-packages\pip\_vendor\pygments\formatter.py                         
  129 .venv\Lib\site-packages\pip\_vendor\packaging\requirements.py                     
  129 .venv\Lib\site-packages\PIL\WalImageFile.py                                       
  129 .venv\Lib\site-packages\numpy\random\tests\test_extending.py                      
  128 .venv\Lib\site-packages\requests\status_codes.py                                  
  128 .venv\Lib\site-packages\pip\_vendor\idna\cli.py                                   
  128 .venv\Lib\site-packages\pip\_vendor\requests\status_codes.py                      
  128 .venv\Lib\site-packages\pip\_internal\network\cache.py                            
  127 .venv\Lib\site-packages\pip\_vendor\requests\help.py                              
  124 .venv\Lib\site-packages\pip\_vendor\urllib3\util\wait.py                          
  124 .venv\Lib\site-packages\PIL\BdfFontFile.py                                        
  124 .venv\Lib\site-packages\pygame\examples\camera.py                                 
  124 .venv\Lib\site-packages\pip\_internal\models\search_scope.py                      
  124 .venv\Lib\site-packages\urllib3\util\wait.py                                      
  123 .venv\Lib\site-packages\pygame\tests\system_test.py                               
  123 .venv\Lib\site-packages\pip\_internal\pyproject.py                                
  123 .venv\Lib\site-packages\numpy\polynomial\tests\test_polyutils.py                  
  122 .venv\Lib\site-packages\pip\_internal\models\target_python.py                     
  122 .venv\Lib\site-packages\numpy\_core\tests\test_indexerrors.py                     
  121 .venv\Lib\site-packages\numpy\_globals.py                                         
  121 .venv\Lib\site-packages\pip\_vendor\cachecontrol\filewrapper.py                   
  121 .venv\Lib\site-packages\numpy\f2py\tests\test_parameter.py                        
  121 .venv\Lib\site-packages\numpy\lib\tests\test_ufunclike.py                         
  120 .venv\Lib\site-packages\pygame\examples\moveit.py                                 
  120 .venv\Lib\site-packages\numpy\_core\_dtype_ctypes.py                              
  120 .venv\Lib\site-packages\pygame\examples\arraydemo.py                              
  120 .venv\Lib\site-packages\PySide6\QtAsyncio\futures.py                              
  119 .venv\Lib\site-packages\pip\_vendor\tomli\_re.py                                  
  117 .venv\Lib\site-packages\pip\_vendor\__init__.py                                   
  116 core\image_loader.py                                                              
  115 config.py                                                                         
  115 ui\main_window_audio.py                                                           
  115 .venv\Lib\site-packages\pygame\examples\blend_fill.py                             
  115 .venv\Lib\site-packages\PIL\FtexImagePlugin.py                                    
  115 .venv\Lib\site-packages\pip\_vendor\rich\theme.py                                 
  113 .venv\Lib\site-packages\PIL\_binary.py                                            
  113 .venv\Lib\site-packages\requests\compat.py                                        
  113 .venv\Lib\site-packages\numpy\_core\tests\test_array_api_info.py                  
  113 .venv\Lib\site-packages\PIL\ImageEnhance.py                                       
  113 ui\main_window.py                                                                 
  113 .venv\Lib\site-packages\pip\_internal\commands\uninstall.py                       
  112 ui\main_window_tray.py                                                            
  112 .venv\Lib\site-packages\PySide6\scripts\qtpy2cpp_lib\astdump.py                   
  110 .venv\Lib\site-packages\numpy\matrixlib\tests\test_matrix_linalg.py               
  109 .venv\Lib\site-packages\pip\_internal\utils\_jaraco_text.py                       
  109 .venv\Lib\site-packages\numpy\f2py\tests\test_return_real.py                      
  109 .venv\Lib\site-packages\pygame\tests\touch_test.py                                
  108 .venv\Lib\site-packages\numpy\_typing\_dtype_like.py                              
  108 .venv\Lib\site-packages\pip\_vendor\packaging\_elffile.py                         
  107 .venv\Lib\site-packages\pip\_internal\commands\freeze.py                          
  106 .venv\Lib\site-packages\pip\_vendor\rich\live_render.py                           
  106 .venv\Lib\site-packages\PySide6\scripts\deploy_lib\deploy_util.py                 
  105 .venv\Lib\site-packages\pip\_internal\req\__init__.py                             
  105 .venv\Lib\site-packages\pygame\examples\sprite_texture.py                         
  105 .venv\Lib\site-packages\numpy\_core\tests\test_simd_module.py                     
  105 .venv\Lib\site-packages\numpy\_core\tests\test_scalarinherit.py                   
  104 .venv\Lib\site-packages\PIL\GdImageFile.py                                        
  104 .venv\Lib\site-packages\pip\_vendor\pygments\scanner.py                           
  104 .venv\Lib\site-packages\pygame\examples\vgrade.py                                 
  103 .venv\Lib\site-packages\PIL\CurImagePlugin.py                                     
  103 .venv\Lib\site-packages\numpy\random\tests\test_seed_sequence.py                  
  103 .venv\Lib\site-packages\PIL\GbrImagePlugin.py                                     
  103 .venv\Lib\site-packages\PIL\ImtImagePlugin.py                                     
  103 .venv\Lib\site-packages\PIL\MicImagePlugin.py                                     
  103 .venv\Lib\site-packages\pip\_internal\build_env\base.py                           
  103 .venv\Lib\site-packages\numpy\typing\tests\test_runtime.py                        
  102 .venv\Lib\site-packages\pip\_vendor\pygments\regexopt.py                          
  102 .venv\Lib\site-packages\pip\_internal\utils\glibc.py                              
  102 .venv\Lib\site-packages\numpy\f2py\tests\test_string.py                           
  101 .venv\Lib\site-packages\pip\_vendor\rich\jupyter.py                               
  101 .venv\Lib\site-packages\urllib3\util\response.py                                  
  101 .venv\Lib\site-packages\pip\_vendor\urllib3\util\response.py                      
  100 .venv\Lib\site-packages\numpy\f2py\use_rules.py                                   
  100 .venv\Lib\site-packages\pip\_vendor\rich\palette.py                               
  100 .venv\Lib\site-packages\numpy\_core\_string_helpers.py                            
   98 .venv\Lib\site-packages\PIL\XbmImagePlugin.py                                     
   98 .venv\Lib\site-packages\pip\_internal\resolution\resolvelib\reporter.py           
   98 .venv\Lib\site-packages\pygame\examples\prevent_display_stretching.py             
   96 .venv\Lib\site-packages\pip\_vendor\requests\compat.py                            
   95 .venv\Lib\site-packages\PySide6\support\generate_pyi.py                           
   95 .venv\Lib\site-packages\numpy\linalg\__init__.py                                  
   95 .venv\Lib\site-packages\numpy\_utils\__init__.py                                  
   95 .venv\Lib\site-packages\pygame\tests\sysfont_test.py                              
   94 .venv\Lib\site-packages\pip\_vendor\rich\_log_render.py                           
   94 .venv\Lib\site-packages\pip\_vendor\packaging\errors.py                           
   94 .venv\Lib\site-packages\numpy\lib\introspect.py                                   
   93 .venv\Lib\site-packages\pygame\examples\liquid.py                                 
   93 .venv\Lib\site-packages\pip\_vendor\rich\bar.py                                   
   93 .venv\Lib\site-packages\pip\_vendor\rich\_wrap.py                                 
   93 .venv\Lib\site-packages\numpy\_typing\_nbit_base.py                               
   92 .venv\Lib\site-packages\pygame\examples\go_over_there.py                          
   92 .venv\Lib\site-packages\pip\_internal\utils\direct_url_helpers.py                 
   92 .venv\Lib\site-packages\numpy\_core\tests\test_umath_accuracy.py                  
   92 .venv\Lib\site-packages\numpy\_typing\_array_like.py                              
   92 .venv\Lib\site-packages\pip\_internal\commands\inspect.py                         
   91 .venv\Lib\site-packages\pip\_internal\utils\compat.py                             
   91 .venv\Lib\site-packages\pip\_internal\models\release_control.py                   
   91 .venv\Lib\site-packages\pygame\examples\setmodescale.py                           
   91 .venv\Lib\site-packages\pip\_vendor\rich\emoji.py                                 
   90 .venv\Lib\site-packages\numpy\typing\tests\data\pass\numeric.py                   
   90 .venv\Lib\site-packages\numpy\lib\__init__.py                                     
   90 .venv\Lib\site-packages\numpy\_core\tests\test_argparse.py                        
   90 .venv\Lib\site-packages\numpy\_core\tests\test__exceptions.py                     
   89 .venv\Lib\site-packages\pygame\tests\test_utils\test_machinery.py                 
   89 .venv\Lib\site-packages\urllib3\filepost.py                                       
   89 .venv\Lib\site-packages\pip\_vendor\urllib3\filepost.py                           
   88 .venv\Lib\site-packages\numpy\random\_pickle.py                                   
   88 .venv\Lib\site-packages\PIL\ImageSequence.py                                      
   88 .venv\Lib\site-packages\pip\_vendor\rich\filesize.py                              
   88 .venv\Lib\site-packages\pip\_internal\utils\entrypoints.py                        
   87 .venv\Lib\site-packages\pip\_vendor\urllib3\http2\probe.py                        
   87 .venv\Lib\site-packages\pip\_internal\metadata\importlib\_compat.py               
   87 .venv\Lib\site-packages\numpy\f2py\tests\test_modules.py                          
   87 .venv\Lib\site-packages\urllib3\http2\probe.py                                    
   87 .venv\Lib\site-packages\pip\_internal\metadata\_json.py                           
   87 .venv\Lib\site-packages\PIL\__init__.py                                           
   87 .venv\Lib\site-packages\pygame\pkgdata.py                                         
   86 .venv\Lib\site-packages\pip\_internal\cli\main.py                                 
   86 .venv\Lib\site-packages\pip\_internal\req\req_dependency_group.py                 
   86 .venv\Lib\site-packages\pygame\examples\fonty.py                                  
   86 .venv\Lib\site-packages\numpy\random\_examples\numba\extending.py                 
   86 .venv\Lib\site-packages\numpy\dtypes.py                                           
   86 .venv\Lib\site-packages\numpy\_core\tests\test_finfo.py                           
   86 .venv\Lib\site-packages\pip\_vendor\rich\scope.py                                 
   85 .venv\Lib\site-packages\numpy\_typing\_nested_sequence.py                         
   85 core\validators.py                                                                
   85 .venv\Lib\site-packages\pip\_vendor\packaging\_musllinux.py                       
   85 .venv\Lib\site-packages\numpy\_core\tests\test_arraymethod.py                     
   85 .venv\Lib\site-packages\PIL\ImageMode.py                                          
   84 .venv\Lib\site-packages\PySide6\QtAsyncio\__init__.py                             
   84 .venv\Lib\site-packages\numpy\testing\overrides.py                                
   84 .venv\Lib\site-packages\PIL\MpegImagePlugin.py                                    
   84 .venv\Lib\site-packages\PIL\DcxImagePlugin.py                                     
   83 ui\modals\kofi_modal.py                                                           
   83 build.py                                                                          
   83 .venv\Lib\site-packages\numpy\ma\tests\test_regression.py                         
   83 .venv\Lib\site-packages\PIL\XVThumbImagePlugin.py                                 
   83 .venv\Lib\site-packages\certifi\core.py                                           
   83 .venv\Lib\site-packages\pip\_vendor\certifi\core.py                               
   82 .venv\Lib\site-packages\pip\_vendor\pygments\__init__.py                          
   82 .venv\Lib\site-packages\pygame\examples\window_opengl.py                          
   82 .venv\Lib\site-packages\pygame\examples\audiocapture.py                           
   82 .venv\Lib\site-packages\pip\_internal\locations\base.py                           
   81 .venv\Lib\site-packages\numpy\tests\test_warnings.py                              
   81 .venv\Lib\site-packages\pip\_internal\utils\egg_link.py                           
   81 .venv\Lib\site-packages\numpy\typing\tests\data\pass\ndarray_conversion.py        
   81 .venv\Lib\site-packages\pip\_internal\req\req_set.py                              
   80 .venv\Lib\site-packages\pygame\tests\imageext_test.py                             
   80 .venv\Lib\site-packages\numpy\lib\tests\test_utils.py                             
   80 .venv\Lib\site-packages\numpy\f2py\__init__.py                                    
   80 .venv\Lib\site-packages\pip\_internal\models\wheel.py                             
   79 .venv\Lib\site-packages\charset_normalizer\legacy.py                              
   79 core\network.py                                                                   
   79 .venv\Lib\site-packages\pygame\examples\dropevent.py                              
   78 .venv\Lib\site-packages\PIL\McIdasImagePlugin.py                                  
   78 .venv\Lib\site-packages\pygame\examples\retro_scaling.py                          
   78 .venv\Lib\site-packages\pygame\freetype.py                                        
   78 .venv\Lib\site-packages\numpy\_expired_attrs_2_0.py                               
   78 .venv\Lib\site-packages\pip\_internal\models\format_control.py                    
   77 .venv\Lib\site-packages\numpy\typing\tests\data\pass\multiarray.py                
   76 .venv\Lib\site-packages\numpy\f2py\tests\test_semicolon_split.py                  
   76 .venv\Lib\site-packages\pip\_vendor\rich\_export_format.py                        
   75 .venv\Lib\site-packages\pip\_vendor\cachecontrol\cache.py                         
   75 .venv\Lib\site-packages\pygame\typing.py                                          
   75 .venv\Lib\site-packages\PIL\GimpPaletteFile.py                                    
   75 .venv\Lib\site-packages\pygame\version.py                                         
   74 .venv\Lib\site-packages\pip\_vendor\pygments\plugin.py                            
   74 .venv\Lib\site-packages\numpy\f2py\tests\test_data.py                             
   73 .venv\Lib\site-packages\numpy\ma\tests\test_deprecations.py                       
   73 .venv\Lib\site-packages\pygame\examples\scrap_clipboard.py                        
   72 .venv\Lib\site-packages\PIL\_deprecate.py                                         
   72 .venv\Lib\site-packages\PIL\Hdf5StubImagePlugin.py                                
   72 .venv\Lib\site-packages\PIL\BufrStubImagePlugin.py                                
   72 .venv\Lib\site-packages\numpy\_core\tests\_locales.py                             
   72 .venv\Lib\site-packages\PIL\GribStubImagePlugin.py                                
   72 .venv\Lib\site-packages\PIL\PixarImagePlugin.py                                   
   71 .venv\Lib\site-packages\pip\_internal\utils\virtualenv.py                         
   71 .venv\Lib\site-packages\pip\_vendor\rich\_windows.py                              
   70 .venv\Lib\site-packages\pip\_vendor\pygments\console.py                           
   70 .venv\Lib\site-packages\pip\_vendor\pygments\filter.py                            
   70 .venv\Lib\site-packages\pygame\docs\serve.py                                      
   70 .venv\Lib\site-packages\pip\_vendor\cachecontrol\_cmd.py                          
   69 .venv\Lib\site-packages\pip\_vendor\rich\_null_file.py                            
   69 .venv\Lib\site-packages\numpy\tests\test_reloading.py                             
   69 core\storage.py                                                                   
   68 .venv\Lib\site-packages\PIL\PcdImagePlugin.py                                     
   68 .venv\Lib\site-packages\pip\_vendor\truststore\_openssl.py                        
   68 ui\design_system.py                                                               
   67 .venv\Lib\site-packages\numpy\random\_examples\numba\extending_distributions.py   
   67 core\autostart.py                                                                 
   67 .venv\Lib\site-packages\numpy\f2py\tests\test_return_complex.py                   
   67 core\paths.py                                                                     
   66 .venv\Lib\site-packages\numpy\f2py\tests\test_return_logical.py                   
   66 .venv\Lib\site-packages\pip\_vendor\platformdirs\__main__.py                      
   66 .venv\Lib\site-packages\pip\_internal\commands\check.py                           
   66 .venv\Lib\site-packages\numpy\f2py\tests\test_docs.py                             
   65 .venv\Lib\site-packages\PySide6\scripts\project_lib\design_studio_project.py      
   64 .venv\Lib\site-packages\numpy\lib\tests\test__version.py                          
   64 .venv\Lib\site-packages\numpy\typing\tests\data\pass\ufunc_config.py              
   63 .venv\Lib\site-packages\PySide6\scripts\qtpy2cpp_lib\qt.py                        
   63 .venv\Lib\site-packages\PySide6\scripts\deploy_lib\commands.py                    
   63 .venv\Lib\site-packages\PySide6\scripts\qtpy2cpp.py                               
   62 .venv\Lib\site-packages\numpy\typing\tests\data\pass\index_tricks.py              
   62 .venv\Lib\site-packages\numpy\f2py\_isocbind.py                                   
   62 .venv\Lib\site-packages\numpy\lib\_array_utils_impl.py                            
   61 .venv\Lib\site-packages\PIL\TarIO.py                                              
   61 .venv\Lib\site-packages\pip\_vendor\pygments\styles\__init__.py                   
   61 .venv\Lib\site-packages\pip\_internal\network\xmlrpc.py                           
   60 scripts\clean_release.py                                                          
   59 .venv\Lib\site-packages\numpy\tests\test_matlib.py                                
   59 .venv\Lib\site-packages\numpy\_core\umath.py                                      
   59 core\api.py                                                                       
   59 tests\test_phase1_p0.py                                                           
   58 .venv\Lib\site-packages\pip\_internal\utils\urls.py                               
   58 .venv\Lib\site-packages\pip\_internal\commands\hash.py                            
   58 .venv\Lib\site-packages\PySide6\scripts\project_lib\pyproject_json.py             
   57 .venv\Lib\site-packages\numpy\typing\tests\data\pass\dtype.py                     
   57 .venv\Lib\site-packages\pip\_internal\models\installation_report.py               
   57 .venv\Lib\site-packages\pip\_vendor\resolvelib\resolvers\exceptions.py            
   57 .venv\Lib\site-packages\pip\_internal\distributions\base.py                       
   57 .venv\Lib\site-packages\pip\_vendor\rich\file_proxy.py                            
   57 core\images.py                                                                    
   57 .venv\Lib\site-packages\numpy\core\_multiarray_umath.py                           
   57 .venv\Lib\site-packages\numpy\f2py\diagnose.py                                    
   56 .venv\Lib\site-packages\pip\_vendor\rich\_windows_renderer.py                     
   56 .venv\Lib\site-packages\PySide6\scripts\qtpy2cpp_lib\tokenizer.py                 
   56 .venv\Lib\site-packages\numpy\f2py\tests\test_isoc.py                             
   55 .venv\Lib\site-packages\numpy\_core\tests\test_multiprocessing.py                 
   55 .venv\Lib\site-packages\numpy\f2py\tests\test_return_integer.py                   
   55 .venv\Lib\site-packages\pip\_vendor\msgpack\__init__.py                           
   55 .venv\Lib\site-packages\pip\_vendor\resolvelib\reporters.py                       
   55 .venv\Lib\site-packages\idna\intranges.py                                         
   55 .venv\Lib\site-packages\pip\_vendor\idna\intranges.py                             
   54 .venv\Lib\site-packages\PIL\PaletteFile.py                                        
   54 .venv\Lib\site-packages\numpy\_core\tests\test_abc.py                             
   54 .venv\Lib\site-packages\pip\_vendor\distro\__init__.py                            
   54 .venv\Lib\site-packages\numpy\tests\test_numpy_version.py                         
   54 .venv\Lib\site-packages\pip\_vendor\pygments\styles\_mapping.py                   
   54 .venv\Lib\site-packages\pip\_vendor\rich\screen.py                                
   53 .venv\Lib\site-packages\pip\_vendor\urllib3\http2\__init__.py                     
   53 .venv\Lib\site-packages\numpy\random\_examples\cffi\parse.py                      
   53 .venv\Lib\site-packages\urllib3\http2\__init__.py                                 
   53 .venv\Lib\site-packages\numpy\ma\__init__.py                                      
   53 .venv\Lib\site-packages\PySide6\scripts\project_lib\__init__.py                   
   53 .venv\Lib\site-packages\pygame\tests\video_test.py                                
   53 .venv\Lib\site-packages\numpy\f2py\tests\test_kind.py                             
   52 .venv\Lib\site-packages\pip\_internal\utils\appdirs.py                            
   52 .venv\Lib\site-packages\numpy\typing\tests\data\pass\ufunclike.py                 
   52 .venv\Lib\site-packages\numpy\f2py\tests\test_assumed_shape.py                    
   52 .venv\Lib\site-packages\numpy\typing\tests\data\pass\literal.py                   
   51 .venv\Lib\site-packages\numpy\tests\test_configtool.py                            
   51 .venv\Lib\site-packages\PySide6\scripts\qtpy2cpp_lib\nodedump.py                  
   51 .venv\Lib\site-packages\pip\_vendor\requests\_internal_utils.py                   
   51 .venv\Lib\site-packages\requests\_internal_utils.py                               
   50 .venv\Lib\site-packages\pip\__pip-runner__.py                                     
   49 .venv\Lib\site-packages\numpy\f2py\tests\test_inplace.py                          
   49 .venv\Lib\site-packages\pygame\examples\resizing_new.py                           
   48 .venv\Lib\site-packages\numpy\f2py\tests\test_return_character.py                 
   48 .venv\Lib\site-packages\pip\_vendor\cachecontrol\caches\redis_cache.py            
   48 .venv\Lib\site-packages\numpy\_core\tests\test_cpu_dispatcher.py                  
   48 .venv\Lib\site-packages\requests\hooks.py                                         
   48 .venv\Lib\site-packages\pip\_vendor\msgpack\exceptions.py                         
   48 .venv\Lib\site-packages\pygame\examples\headless_no_windows_needed.py             
   48 .venv\Lib\site-packages\charset_normalizer\__init__.py                            
   48 .venv\Lib\site-packages\pip\_vendor\requests\hooks.py                             
   48 .venv\Lib\site-packages\pip\_vendor\resolvelib\resolvers\criterion.py             
   47 .venv\Lib\site-packages\numpy\typing\tests\data\pass\ndarray_shape_manipulation.py
   47 .venv\Lib\site-packages\pygame\examples\sound.py                                  
   47 .venv\Lib\site-packages\idna\__init__.py                                          
   47 .venv\Lib\site-packages\pip\_vendor\resolvelib\resolvers\abstract.py              
   47 .venv\Lib\site-packages\pip\_internal\operations\build\wheel_editable.py          
   47 .venv\Lib\site-packages\numpy\tests\test_numpy_config.py                          
   46 .venv\Lib\site-packages\numpy\_core\tests\test_protocols.py                       
   46 .venv\Lib\site-packages\pip\_internal\utils\retry.py                              
   46 .venv\Lib\site-packages\pygame\tests\image__save_gl_surface_test.py               
   46 .venv\Lib\site-packages\pygame\examples\aacircle.py                               
   45 .venv\Lib\site-packages\pip\_internal\distributions\wheel.py                      
   45 .venv\Lib\site-packages\pygame\__pyinstaller\hook-pygame.py                       
   45 .venv\Lib\site-packages\numpy\lib\tests\test_arrayterator.py                      
   45 .venv\Lib\site-packages\pip\_vendor\idna\__init__.py                              
   45 .venv\Lib\site-packages\numpy\tests\test_scripts.py                               
   45 .venv\Lib\site-packages\PIL\_typing.py                                            
   45 .venv\Lib\site-packages\numpy\typing\tests\data\pass\modules.py                   
   44 .venv\Lib\site-packages\pip\_internal\utils\packaging.py                          
   44 .venv\Lib\site-packages\numpy\random\_examples\cffi\extending.py                  
   44 tests\test_integration_e2e.py                                                     
   44 .venv\Lib\site-packages\numpy\f2py\_backends\_backend.py                          
   43 .venv\Lib\site-packages\idna\compat.py                                            
   43 .venv\Lib\site-packages\pip\_vendor\cachecontrol\wrapper.py                       
   43 .venv\Lib\site-packages\numpy\f2py\tests\test_pyf_src.py                          
   43 .venv\Lib\site-packages\pip\_vendor\rich\_loop.py                                 
   43 .venv\Lib\site-packages\pip\_vendor\urllib3\util\proxy.py                         
   43 .venv\Lib\site-packages\pip\_vendor\pygments\modeline.py                          
   43 .venv\Lib\site-packages\urllib3\util\proxy.py                                     
   42 .venv\Lib\site-packages\pip\_vendor\urllib3\util\util.py                          
   42 .venv\Lib\site-packages\urllib3\util\__init__.py                                  
   42 .venv\Lib\site-packages\pip\_internal\build_env\noop.py                           
   42 .venv\Lib\site-packages\pip\_vendor\rich\protocol.py                              
   42 .venv\Lib\site-packages\urllib3\util\util.py                                      
   42 .venv\Lib\site-packages\pip\_internal\models\direct_url.py                        
   42 .venv\Lib\site-packages\pip\_vendor\rich\styled.py                                
   42 .venv\Lib\site-packages\pip\_vendor\urllib3\util\__init__.py                      
   42 .venv\Lib\site-packages\numpy\f2py\tests\test_size.py                             
   41 .venv\Lib\site-packages\pip\_internal\operations\build\metadata_editable.py       
   41 .venv\Lib\site-packages\pip\_internal\req\pep723.py                               
   41 .venv\Lib\site-packages\pip\_vendor\idna\compat.py                                
   40 .venv\Lib\site-packages\pip\_internal\commands\help.py                            
   40 .venv\Lib\site-packages\numpy\ma\tests\test_arrayobject.py                        
   40 .venv\Lib\site-packages\pygame\tests\__init__.py                                  
   39 tests\test_phase2_p1.py                                                           
   39 .venv\Lib\site-packages\numpy\_core\tests\examples\cython\setup.py                
   39 .venv\Lib\site-packages\numpy\_configtool.py                                      
   39 .venv\Lib\site-packages\pip\_vendor\rich\diagnose.py                              
   38 .venv\Lib\site-packages\pip\_internal\operations\build\metadata.py                
   38 core\ui_settings.py                                                               
   38 .venv\Lib\site-packages\pip\_internal\utils\_log.py                               
   38 .venv\Lib\site-packages\pip\_internal\operations\build\wheel.py                   
   38 .venv\Lib\site-packages\pip\_vendor\rich\color_triplet.py                         
   37 .venv\Lib\site-packages\numpy\typing\tests\data\pass\arrayprint.py                
   37 .venv\Lib\site-packages\numpy\typing\tests\data\pass\array_like.py                
   37 .venv\Lib\site-packages\pip\_vendor\rich\constrain.py                             
   36 .venv\Lib\site-packages\numpy\typing\tests\data\pass\einsumfunc.py                
   36 .venv\Lib\site-packages\pip\_internal\models\selection_prefs.py                   
   36 .venv\Lib\site-packages\pip\_vendor\truststore\__init__.py                        
   35 .venv\Lib\site-packages\pygame\tests\docs_test.py                                 
   35 .venv\Lib\site-packages\numpy\tests\test_lazyloading.py                           
   35 .venv\Lib\site-packages\numpy\typing\tests\test_isfile.py                         
   35 .venv\Lib\site-packages\numpy\_pyinstaller\tests\test_pyinstaller.py              
   35 .venv\Lib\site-packages\numpy\_pyinstaller\hook-numpy.py                          
   34 .venv\Lib\site-packages\pip\_internal\distributions\installed.py                  
   34 .venv\Lib\site-packages\pip\_vendor\rich\pager.py                                 
   34 tests\test_phase3_ux.py                                                           
   34 .venv\Lib\site-packages\pip\_vendor\rich\errors.py                                
   33 .venv\Lib\site-packages\numpy\core\__init__.py                                    
   33 .venv\Lib\site-packages\pip\_vendor\rich\abc.py                                   
   33 .venv\Lib\site-packages\pip\_vendor\distlib\__init__.py                           
   33 .venv\Lib\site-packages\pip\_vendor\packaging\_structures.py                      
   32 .venv\Lib\site-packages\pip\_vendor\cachecontrol\__init__.py                      
   32 .venv\Lib\site-packages\pip\_vendor\rich\_emoji_replace.py                        
   32 .venv\Lib\site-packages\numpy\lib\tests\test_array_utils.py                       
   32 .venv\Lib\site-packages\numpy\_core\printoptions.py                               
   32 .venv\Lib\site-packages\numpy\_pyinstaller\tests\pyinstaller-smoke.py             
   31 .venv\Lib\site-packages\pip\_vendor\pyproject_hooks\__init__.py                   
   31 .venv\Lib\site-packages\numpy\char\__init__.py                                    
   31 .venv\Lib\site-packages\numpy\f2py\tests\test_mixed.py                            
   31 .venv\Lib\site-packages\pip\_vendor\truststore\_ssl_constants.py                  
   31 .venv\Lib\site-packages\numpy\matrixlib\tests\test_regression.py                  
   30 .venv\Lib\site-packages\pygame\locals.py                                          
   30 .venv\Lib\site-packages\pygame\tests\version_test.py                              
   29 .venv\Lib\site-packages\numpy\f2py\tests\test_routines.py                         
   29 .venv\Lib\site-packages\PIL\_util.py                                              
   28 .venv\Lib\site-packages\pygame\_sprite.py                                         
   28 .venv\Lib\site-packages\numpy\typing\tests\data\pass\arrayterator.py              
   28 .venv\Lib\site-packages\pip\_internal\utils\datetime.py                           
   28 .venv\Lib\site-packages\pip\_internal\models\index.py                             
   28 .venv\Lib\site-packages\pip\_internal\cli\command_context.py                      
   27 .venv\Lib\site-packages\shiboken6\__init__.py                                     
   27 .venv\Lib\site-packages\numpy\core\_internal.py                                   
   27 .venv\Lib\site-packages\pip\_vendor\resolvelib\__init__.py                        
   27 .venv\Lib\site-packages\pip\_internal\models\candidate.py                         
   27 .venv\Lib\site-packages\pip\_vendor\resolvelib\resolvers\__init__.py              
   26 .venv\Lib\site-packages\pygame\tests\typing_test.py                               
   26 .venv\Lib\site-packages\pygame\docs\static.py                                     
   26 .venv\Lib\site-packages\numpy\typing\tests\data\pass\flatiter.py                  
   26 .venv\Lib\site-packages\numpy\f2py\tests\test_abstract_interface.py               
   25 .venv\Lib\site-packages\numpy\core\multiarray.py                                  
   25 .venv\Lib\site-packages\pip\_internal\build_env\__init__.py                       
   25 .venv\Lib\site-packages\pip\_vendor\requests\packages.py                          
   24 .venv\Lib\site-packages\numpy\f2py\tests\test_common.py                           
   24 .venv\Lib\site-packages\numpy\_core\tests\examples\limited_api\setup.py           
   24 .venv\Lib\site-packages\urllib3\_version.py                                       
   24 .venv\Lib\site-packages\pip\_vendor\urllib3\_version.py                           
   24 .venv\Lib\site-packages\pygame\tests\debug_test.py                                
   24 .venv\Lib\site-packages\pip\_vendor\platformdirs\version.py                       
   24 .venv\Lib\site-packages\numpy\lib\format.py                                       
   24 .venv\Lib\site-packages\pip\__main__.py                                           
   24 .venv\Lib\site-packages\pip\_internal\utils\filetypes.py                          
   24 .venv\Lib\site-packages\pip\_vendor\rich\_fileno.py                               
   23 .venv\Lib\site-packages\requests\packages.py                                      
   23 .venv\Lib\site-packages\pip\_internal\models\scheme.py                            
   23 .venv\Lib\site-packages\pip\_vendor\pygments\formatters\_mapping.py               
   22 .venv\Lib\site-packages\numpy\testing\__init__.py                                 
   22 .venv\Lib\site-packages\numpy\typing\tests\data\pass\lib_user_array.py            
   22 .venv\Lib\site-packages\pip\_vendor\urllib3\contrib\emscripten\request.py         
   22 .venv\Lib\site-packages\urllib3\contrib\emscripten\request.py                     
   21 .venv\Lib\site-packages\pip\_internal\distributions\__init__.py                   
   21 .venv\Lib\site-packages\pip\_vendor\pyproject_hooks\_in_process\__init__.py       
   21 .venv\Lib\site-packages\numpy\linalg\tests\test_deprecations.py                   
   21 .venv\Lib\site-packages\numpy\core\_utils.py                                      
   20 .venv\Lib\site-packages\PySide6\_git_pyside_version.py                            
   20 .venv\Lib\site-packages\PIL\_tkinter_finder.py                                    
   20 .venv\Lib\site-packages\PIL\ImagePath.py                                          
   20 .venv\Lib\site-packages\pip\_internal\resolution\base.py                          
   20 .venv\Lib\site-packages\shiboken6\_git_shiboken_module_version.py                 
   20 .venv\Lib\site-packages\numpy\f2py\tests\test_f2cmap.py                           
   20 .venv\Lib\site-packages\numpy\_typing\_scalars.py                                 
   19 .venv\Lib\site-packages\PySide6\support\deprecated.py                             
   19 .venv\Lib\site-packages\pip\_vendor\rich\_timer.py                                
   19 .venv\Lib\site-packages\numpy\f2py\tests\test_quoted_character.py                 
   19 .venv\Lib\site-packages\numpy\typing\tests\data\pass\shape.py                     
   19 .venv\Lib\site-packages\numpy\typing\tests\data\pass\lib_utils.py                 
   18 .venv\Lib\site-packages\pip\_vendor\requests\certs.py                             
   18 .venv\Lib\site-packages\numpy\_utils\_conversions.py                              
   18 .venv\Lib\site-packages\certifi\tests\test_certify.py                             
   18 .venv\Lib\site-packages\numpy\matrixlib\tests\test_numeric.py                     
   18 .venv\Lib\site-packages\pip\_internal\__init__.py                                 
   18 .venv\Lib\site-packages\requests\certs.py                                         
   18 .venv\Lib\site-packages\numpy\typing\tests\data\pass\lib_version.py               
   18 .venv\Lib\site-packages\pygame\tests\ftfont_test.py                               
   17 .venv\Lib\site-packages\pygame\docs\__main__.py                                   
   17 .venv\Lib\site-packages\numpy\matrixlib\tests\test_multiarray.py                  
   17 .venv\Lib\site-packages\pip\_vendor\pygments\__main__.py                          
   17 .venv\Lib\site-packages\pip\_vendor\rich\_pick.py                                 
   17 .venv\Lib\site-packages\numpy\_typing\_nbit.py                                    
   17 .venv\Lib\site-packages\pip\_vendor\urllib3\contrib\emscripten\__init__.py        
   17 .venv\Lib\site-packages\urllib3\contrib\emscripten\__init__.py                    
   17 .venv\Lib\site-packages\PySide6\_config.py                                        
   17 .venv\Lib\site-packages\pygame\tests\locals_test.py                               
   17 .venv\Lib\site-packages\pygame\tests\ctest_test.py                                
   17 .venv\Lib\site-packages\numpy\typing\tests\data\pass\numerictypes.py              
   16 .venv\Lib\site-packages\numpy\_pyinstaller\tests\__init__.py                      
   16 .venv\Lib\site-packages\numpy\typing\tests\data\pass\ufuncs.py                    
   16 .venv\Lib\site-packages\numpy\f2py\tests\__init__.py                              
   16 .venv\Lib\site-packages\numpy\f2py\tests\test_block_docstring.py                  
   16 .venv\Lib\site-packages\pip\_vendor\rich\_stack.py                                
   15 .venv\Lib\site-packages\numpy\f2py\tests\test_value_attrspec.py                   
   15 .venv\Lib\site-packages\pip\_internal\vcs\__init__.py                             
   15 .venv\Lib\site-packages\numpy\_typing\_extended_precision.py                      
   15 .venv\Lib\site-packages\numpy\_distributor_init.py                                
   15 .venv\Lib\site-packages\pip\_vendor\packaging\__init__.py                         
   14 .venv\Lib\site-packages\requests\__version__.py                                   
   14 .venv\Lib\site-packages\pip\_vendor\requests\__version__.py                       
   13 .venv\Lib\site-packages\numpy\_core\cversions.py                                  
   13 .venv\Lib\site-packages\numpy\lib\scimath.py                                      
   13 .venv\Lib\site-packages\numpy\ctypeslib\__init__.py                               
   13 .venv\Lib\site-packages\pygame\_data_classes.py                                   
   13 .venv\Lib\site-packages\pygame\macosx.py                                          
   13 .venv\Lib\site-packages\pip\__init__.py                                           
   12 .venv\Lib\site-packages\pip\_vendor\certifi\__main__.py                           
   12 .venv\Lib\site-packages\certifi\__main__.py                                       
   12 .venv\Lib\site-packages\numpy\matrixlib\__init__.py                               
   12 .venv\Lib\site-packages\PySide6\scripts\project_lib\pyproject_parse_result.py     
   12 .venv\Lib\site-packages\shiboken6\_config.py                                      
   12 .venv\Lib\site-packages\numpy\core\numeric.py                                     
   12 .venv\Lib\site-packages\pip\_internal\main.py                                     
   11 .venv\Lib\site-packages\pygame\tests\surfarray_tags.py                            
   11 .venv\Lib\site-packages\pygame\tests\sndarray_tags.py                             
   11 .venv\Lib\site-packages\numpy\version.py                                          
   10 .venv\Lib\site-packages\numpy\core\getlimits.py                                   
   10 .venv\Lib\site-packages\pip\_vendor\tomli\_types.py                               
   10 .venv\Lib\site-packages\numpy\tests\test__all__.py                                
   10 .venv\Lib\site-packages\numpy\core\function_base.py                               
   10 .venv\Lib\site-packages\numpy\core\shape_base.py                                  
   10 .venv\Lib\site-packages\numpy\core\fromnumeric.py                                 
   10 .venv\Lib\site-packages\numpy\f2py\tests\test_capi_maps.py                        
   10 .venv\Lib\site-packages\numpy\core\_dtype_ctypes.py                               
   10 .venv\Lib\site-packages\numpy\core\_dtype.py                                      
   10 .venv\Lib\site-packages\numpy\core\umath.py                                       
   10 .venv\Lib\site-packages\numpy\core\records.py                                     
   10 .venv\Lib\site-packages\pygame\docs\__init__.py                                   
   10 .venv\Lib\site-packages\numpy\core\numerictypes.py                                
   10 .venv\Lib\site-packages\numpy\core\overrides.py                                   
   10 .venv\Lib\site-packages\numpy\core\einsumfunc.py                                  
   10 .venv\Lib\site-packages\pip\_vendor\rich\_extension.py                            
   10 .venv\Lib\site-packages\numpy\core\arrayprint.py                                  
   10 .venv\Lib\site-packages\numpy\core\defchararray.py                                
   10 .venv\Lib\site-packages\pip\_vendor\rich\region.py                                
    8 .venv\Lib\site-packages\charset_normalizer\cli\__init__.py                        
    8 .venv\Lib\site-packages\charset_normalizer\version.py                             
    8 .venv\Lib\site-packages\numpy\_typing\_shape.py                                   
    8 .venv\Lib\site-packages\pip\_vendor\tomli\__init__.py                             
    8 .venv\Lib\site-packages\pip\_vendor\cachecontrol\caches\__init__.py               
    7 .venv\Lib\site-packages\numpy\_typing\_ufunc.py                                   
    7 .venv\Lib\site-packages\PySide6\support\__init__.py                               
    7 .venv\Lib\site-packages\PIL\__main__.py                                           
    7 .venv\Lib\site-packages\numpy\lib\array_utils.py                                  
    7 .venv\Lib\site-packages\pip\_internal\cli\status_codes.py                         
    6 .venv\Lib\site-packages\pip\_vendor\idna\__main__.py                              
    6 .venv\Lib\site-packages\pip\_internal\metadata\importlib\__init__.py              
    6 .venv\Lib\site-packages\numpy\f2py\_backends\__init__.py                          
    6 .venv\Lib\site-packages\numpy\typing\tests\data\pass\warnings_and_errors.py       
    6 .venv\Lib\site-packages\charset_normalizer\__main__.py                            
    6 .venv\Lib\site-packages\idna\__main__.py                                          
    5 .venv\Lib\site-packages\pip\_vendor\rich\themes.py                                
    5 .venv\Lib\site-packages\pygame\tests\camera_test.py                               
    5 .venv\Lib\site-packages\numpy\f2py\__main__.py                                    
    5 .venv\Lib\site-packages\pygame\__pyinstaller\__init__.py                          
    5 .venv\Lib\site-packages\PIL\report.py                                             
    4 .venv\Lib\site-packages\PIL\_version.py                                           
    4 .venv\Lib\site-packages\pip\_vendor\tomli_w\__init__.py                           
    4 .venv\Lib\site-packages\pip\_vendor\distro\__main__.py                            
    4 .venv\Lib\site-packages\pip\_vendor\certifi\__init__.py                           
    4 .venv\Lib\site-packages\numpy\typing\tests\data\pass\nditer.py                    
    4 .venv\Lib\site-packages\certifi\__init__.py                                       
    4 .venv\Lib\site-packages\pygame\_sdl2\__init__.py                                  
    3 .venv\Lib\site-packages\pip\_internal\cli\__init__.py                             
    2 .venv\Lib\site-packages\numpy\rec\__init__.py                                     
    2 .venv\Lib\site-packages\numpy\strings\__init__.py                                 
    1 .venv\Lib\site-packages\numpy\lib\user_array.py                                   
    1 .venv\Lib\site-packages\pip\_internal\index\__init__.py                           
    1 .venv\Lib\site-packages\idna\package_data.py                                      
    1 .venv\Lib\site-packages\pip\_vendor\idna\package_data.py                          
    1 .venv\Lib\site-packages\numpy\lib\stride_tricks.py                                
    1 .venv\Lib\site-packages\pip\_internal\network\__init__.py                         
    1 .venv\Lib\site-packages\pip\_internal\operations\install\__init__.py              
    1 .venv\Lib\site-packages\numpy\f2py\__version__.py                                 
    1 .venv\Lib\site-packages\numpy\lib\npyio.py                                        
    1 .venv\Lib\site-packages\pip\_internal\models\__init__.py                          
    1 .venv\Lib\site-packages\pygame\_sdl2\window.py                                    
    0 .venv\Lib\site-packages\pygame\__briefcase\__init__.py                            
    0 tests\__init__.py                                                                 
    0 .venv\Lib\site-packages\numpy\linalg\tests\__init__.py                            
    0 ui\__init__.py                                                                    
    0 .venv\Lib\site-packages\PySide6\scripts\__init__.py                               
    0 .venv\Lib\site-packages\numpy\tests\__init__.py                                   
    0 .venv\Lib\site-packages\numpy\ma\tests\__init__.py                                
    0 .venv\Lib\site-packages\certifi\tests\__init__.py                                 
    0 .venv\Lib\site-packages\numpy\typing\tests\__init__.py                            
    0 .venv\Lib\site-packages\numpy\lib\tests\__init__.py                               
    0 .venv\Lib\site-packages\pip\_internal\operations\build\__init__.py                
    0 .venv\Lib\site-packages\numpy\testing\tests\__init__.py                           
    0 .venv\Lib\site-packages\pip\_internal\operations\__init__.py                      
    0 .venv\Lib\site-packages\pygame\examples\__init__.py                               
    0 .venv\Lib\site-packages\pip\_internal\resolution\__init__.py                      
    0 .venv\Lib\site-packages\pip\_internal\resolution\legacy\__init__.py               
    0 .venv\Lib\site-packages\urllib3\contrib\__init__.py                               
    0 .venv\Lib\site-packages\numpy\testing\_private\__init__.py                        
    0 .venv\Lib\site-packages\pip\_internal\resolution\resolvelib\__init__.py           
    0 .venv\Lib\site-packages\pip\_internal\utils\__init__.py                           
    0 core\scrapers\__init__.py                                                         
    0 core\__init__.py                                                                  
    0 .venv\Lib\site-packages\numpy\fft\tests\__init__.py                               
    0 .venv\Lib\site-packages\numpy\matrixlib\tests\__init__.py                         
    0 .venv\Lib\site-packages\numpy\polynomial\tests\__init__.py                        
    0 .venv\Lib\site-packages\pip\_vendor\urllib3\contrib\__init__.py                   
    0 .venv\Lib\site-packages\numpy\random\tests\data\__init__.py                       
    0 .venv\Lib\site-packages\numpy\random\tests\__init__.py                            
    0 .venv\Lib\site-packages\numpy\_pyinstaller\__init__.py                            



```

## 5. Tests and syntax

### Python version

```text
Python 3.14.7
```

### Unittest discovery

```text
[No output]
```

### Compileall

```text
[No output]
```

Pytest: no pytest.ini or pyproject.toml detected.

## 6. Dependencies

### requirements.txt

```text
certifi==2026.7.22
charset-normalizer==3.5.1
idna==3.19
numpy==2.5.3
pillow==12.3.0
plyer==2.1.0
pygame-ce==2.5.8
PySide6==6.11.2
PySide6_Addons==6.11.2
PySide6_Essentials==6.11.2
requests==2.34.2
shiboken6==6.11.2
urllib3==2.7.0
```

### Installed Python packages

```text
boolean.py==5.0
CacheControl==0.14.4
certifi==2026.7.22
charset-normalizer==3.5.1
cyclonedx-python-lib==11.12.0
defusedxml==0.7.1
filelock==3.32.6
idna==3.19
license-expression==30.4.4
markdown-it-py==4.2.0
mdurl==0.1.2
msgpack==1.2.2
numpy==2.5.3
packageurl-python==0.17.6
packaging==26.3
pillow==12.3.0
pip-requirements-parser==32.0.1
pip_api==0.0.35
pip_audit==2.10.1
platformdirs==4.11.8
plyer==2.1.0
py-serializable==2.1.0
pygame-ce==2.5.8
Pygments==2.21.0
pyparsing==3.3.2
PySide6==6.11.2
PySide6_Addons==6.11.2
PySide6_Essentials==6.11.2
requests==2.34.2
rich==15.0.0
shiboken6==6.11.2
sortedcontainers==2.4.0
tomli==2.4.1
tomli_w==1.2.0
urllib3==2.7.0
```


## 7. Static security scan

### Pattern: verify\s*=\s*False

```text
.venv\Lib\site-packages\numpy\lib\_ufunclike_impl.py:18: @array_function_dispatch(_dispatcher, verify=False, module='numpy')
.venv\Lib\site-packages\numpy\lib\_ufunclike_impl.py:75: @array_function_dispatch(_dispatcher, verify=False, module='numpy')
.venv\Lib\site-packages\numpy\lib\_ufunclike_impl.py:145: @array_function_dispatch(_dispatcher, verify=False, module='numpy')
.venv\Lib\site-packages\numpy\_core\multiarray.py:112: module='numpy', docs_from_dispatcher=True, verify=False)
.venv\Lib\site-packages\numpy\_core\tests\test_overrides.py:294: @array_function_dispatch(lambda x: (x,), verify=False)
.venv\Lib\site-packages\pip\_internal\network\session.py:292: super().cert_verify(conn=conn, url=url, verify=False, cert=cert)
.venv\Lib\site-packages\pip\_internal\network\session.py:303: super().cert_verify(conn=conn, url=url, verify=False, cert=cert)
```

### Pattern: shell\s*=\s*True

```text
.venv\Lib\site-packages\pip\_internal\commands\configuration.py:248: subprocess.check_call(f'{editor} "{fname}"', shell=True)
.venv\Lib\site-packages\pygame\_camera_opencv.py:19: shell=True,
```

### Pattern: subprocess\.

```text
build.py:18: result = subprocess.run(cmd, cwd=ROOT_DIR)
.venv\Lib\site-packages\numpy\conftest.py:114: tr.line("code that re-enables the GIL should do so in a subprocess.")
.venv\Lib\site-packages\numpy\f2py\tests\test_f2py2e.py:528: subprocess.check_call(cmd, cwd=tmp_path)
.venv\Lib\site-packages\numpy\f2py\tests\test_f2py2e.py:617: rout = subprocess.run(cmd_run, capture_output=True, encoding='UTF-8')
.venv\Lib\site-packages\numpy\f2py\tests\test_f2py2e.py:806: rout = subprocess.run(cmd_run, capture_output=True, encoding='UTF-8')
.venv\Lib\site-packages\numpy\f2py\tests\test_f2py2e.py:829: rout = subprocess.run(cmd_run, capture_output=True, encoding='UTF-8')
.venv\Lib\site-packages\numpy\f2py\tests\test_f2py2e.py:854: rout = subprocess.run(cmd_run, capture_output=True, encoding='UTF-8')
.venv\Lib\site-packages\numpy\f2py\tests\util.py:50: runmeson = subprocess.run(
.venv\Lib\site-packages\numpy\f2py\tests\util.py:56: except subprocess.CalledProcessError:
.venv\Lib\site-packages\numpy\f2py\tests\util.py:246: p = subprocess.Popen(cmd,
.venv\Lib\site-packages\numpy\f2py\tests\util.py:247: stdout=subprocess.PIPE,
.venv\Lib\site-packages\numpy\f2py\tests\util.py:248: stderr=subprocess.STDOUT)
.venv\Lib\site-packages\numpy\f2py\tests\util.py:267: subprocess.check_call(
.venv\Lib\site-packages\numpy\f2py\_backends\_meson.py:185: subprocess.run(command, cwd=cwd, check=True)
.venv\Lib\site-packages\numpy\testing\_private\utils.py:1486: output = subprocess.run(cmd, capture_output=True, text=True)
.venv\Lib\site-packages\numpy\testing\_private\utils.py:1488: except (OSError, subprocess.SubprocessError):
.venv\Lib\site-packages\numpy\testing\_private\utils.py:2881: Returns the ``subprocess.CompletedProcess`` for callers that want to
.venv\Lib\site-packages\numpy\testing\_private\utils.py:2883: ``subprocess.run``.
.venv\Lib\site-packages\numpy\testing\_private\utils.py:2889: res = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True,
.venv\Lib\site-packages\numpy\tests\test_configtool.py:23: p = subprocess.run(['numpy-config', arg], capture_output=True, text=True)
.venv\Lib\site-packages\numpy\tests\test_scripts.py:38: stdout = subprocess.check_output([f2py_cmd, '-v'])
.venv\Lib\site-packages\numpy\tests\test_scripts.py:44: stdout = subprocess.check_output([sys.executable, '-mnumpy.f2py', '-v'])
.venv\Lib\site-packages\numpy\_core\tests\test_cpu_features.py:31: auxv = subprocess.check_output(['/bin/true'], env={"LD_SHOW_AUXV": "1"})
.venv\Lib\site-packages\numpy\_core\tests\test_cpu_features.py:113: auxv = subprocess.check_output(['/bin/true'], env={"LD_SHOW_AUXV": "1"})
.venv\Lib\site-packages\numpy\_core\tests\test_cpu_features.py:169: return subprocess.run(
.venv\Lib\site-packages\numpy\_core\tests\test_cpu_features.py:184: except subprocess.CalledProcessError as e:
.venv\Lib\site-packages\numpy\_core\tests\test_cython.py:66: subprocess.check_call(["meson", "--version"])
.venv\Lib\site-packages\numpy\_core\tests\test_limited_api.py:66: subprocess.check_call(["meson", "--version"])
.venv\Lib\site-packages\numpy\_core\tests\test_multiarray.py:6789: subprocess.check_output([sys.executable, "-c", code],
.venv\Lib\site-packages\numpy\_core\tests\test_multiarray.py:6790: stderr=subprocess.STDOUT, text=True)
.venv\Lib\site-packages\numpy\_core\tests\test_multiarray.py:6791: except subprocess.CalledProcessError as e:
.venv\Lib\site-packages\numpy\_core\tests\test_multithreading.py:554: except subprocess.TimeoutExpired:
.venv\Lib\site-packages\numpy\_core\tests\test_nditer.py:2237: res = subprocess.check_output([sys.executable, "-c", code],
.venv\Lib\site-packages\numpy\_core\tests\test_nditer.py:2238: stderr=subprocess.STDOUT, text=True)
.venv\Lib\site-packages\numpy\_pyinstaller\tests\test_pyinstaller.py:34: p = subprocess.run([str(exe)], check=True, stdout=subprocess.PIPE)
.venv\Lib\site-packages\PIL\EpsImagePlugin.py:61: subprocess.check_call(["gs", "--version"], stdout=subprocess.DEVNULL)
.venv\Lib\site-packages\PIL\EpsImagePlugin.py:157: startupinfo = subprocess.STARTUPINFO()
.venv\Lib\site-packages\PIL\EpsImagePlugin.py:158: startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
.venv\Lib\site-packages\PIL\EpsImagePlugin.py:159: subprocess.check_call(command, startupinfo=startupinfo)
.venv\Lib\site-packages\PIL\GifImagePlugin.py:888: subprocess.check_call(
.venv\Lib\site-packages\PIL\GifImagePlugin.py:889: ["ppmtogif", tempfile], stdout=f, stderr=subprocess.DEVNULL
.venv\Lib\site-packages\PIL\GifImagePlugin.py:896: quant_proc = subprocess.Popen(
.venv\Lib\site-packages\PIL\GifImagePlugin.py:897: quant_cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL
.venv\Lib\site-packages\PIL\GifImagePlugin.py:899: togif_proc = subprocess.Popen(
.venv\Lib\site-packages\PIL\GifImagePlugin.py:903: stderr=subprocess.DEVNULL,
.venv\Lib\site-packages\PIL\GifImagePlugin.py:912: raise subprocess.CalledProcessError(retcode, quant_cmd)
.venv\Lib\site-packages\PIL\ImageShow.py:328: subprocess.Popen(args)
.venv\Lib\site-packages\PIL\JpegImagePlugin.py:474: subprocess.check_call(["djpeg", "-outfile", path, self.filename])
.venv\Lib\site-packages\pip\_internal\build_env\installer.py:39: Install build dependencies by calling pip in a subprocess.
.venv\Lib\site-packages\pip\_internal\cli\main.py:46: # which imports __main__ for each spawned subprocess.
.venv\Lib\site-packages\pip\_internal\cli\main_parser.py:102: proc = subprocess.run(pip_cmd)
.venv\Lib\site-packages\pip\_internal\cli\main_parser.py:104: except (subprocess.SubprocessError, OSError) as exc:
.venv\Lib\site-packages\pip\_internal\commands\configuration.py:248: subprocess.check_call(f'{editor} "{fname}"', shell=True)
.venv\Lib\site-packages\pip\_internal\commands\configuration.py:253: except subprocess.CalledProcessError as e:
.venv\Lib\site-packages\pip\_internal\network\auth.py:138: res = subprocess.run(  # noqa: UP022
.venv\Lib\site-packages\pip\_internal\network\auth.py:140: stdin=subprocess.DEVNULL,
.venv\Lib\site-packages\pip\_internal\network\auth.py:141: stdout=subprocess.PIPE,
.venv\Lib\site-packages\pip\_internal\network\auth.py:142: stderr=subprocess.PIPE,
.venv\Lib\site-packages\pip\_internal\network\auth.py:171: subprocess.run(
.venv\Lib\site-packages\pip\_internal\network\session.py:157: rustc_output = subprocess.check_output(
.venv\Lib\site-packages\pip\_internal\utils\subprocess.py:133: stdout=subprocess.PIPE,
.venv\Lib\site-packages\pip\_internal\utils\subprocess.py:134: stderr=subprocess.STDOUT if not stdout_only else subprocess.PIPE,
.venv\Lib\site-packages\pip\_vendor\distlib\util.py:1785: p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, **kwargs)
.venv\Lib\site-packages\pip\_vendor\distro\distro.py:1165: stdout = subprocess.check_output(cmd, stderr=subprocess.DEVNULL)
.venv\Lib\site-packages\pip\_vendor\distro\distro.py:1167: except (OSError, subprocess.CalledProcessError):
.venv\Lib\site-packages\pip\_vendor\distro\distro.py:1202: stdout = subprocess.check_output(cmd, stderr=subprocess.DEVNULL)
.venv\Lib\site-packages\pip\_vendor\distro\distro.py:1213: stdout = subprocess.check_output("oslevel", stderr=subprocess.DEVNULL)
.venv\Lib\site-packages\pip\_vendor\distro\distro.py:1214: except (OSError, subprocess.CalledProcessError):
.venv\Lib\site-packages\pip\_vendor\packaging\tags.py:608: version_str = subprocess.run(
.venv\Lib\site-packages\pip\_vendor\packaging\tags.py:617: stdout=subprocess.PIPE,
.venv\Lib\site-packages\pip\_vendor\packaging\_musllinux.py:52: proc = subprocess.run([ld], check=False, stderr=subprocess.PIPE, text=True)
.venv\Lib\site-packages\pip\_vendor\pyproject_hooks\_impl.py:75: """The default method of calling the wrapper subprocess.
.venv\Lib\site-packages\pip\_vendor\pyproject_hooks\_impl.py:93: This uses :func:`subprocess.check_output` under the hood.
.venv\Lib\site-packages\pygame\sysfont.py:219: proc = subprocess.run(
.venv\Lib\site-packages\pygame\sysfont.py:221: stdout=subprocess.PIPE,  # capture stdout
.venv\Lib\site-packages\pygame\sysfont.py:222: stderr=subprocess.PIPE,  # capture stderr
.venv\Lib\site-packages\pygame\sysfont.py:232: except subprocess.TimeoutExpired:
.venv\Lib\site-packages\pygame\sysfont.py:238: except subprocess.CalledProcessError as e:
.venv\Lib\site-packages\pygame\_camera_opencv.py:17: flout, _ = subprocess.Popen(
.venv\Lib\site-packages\pygame\_camera_opencv.py:20: stdout=subprocess.PIPE,
.venv\Lib\site-packages\pygame\_camera_opencv.py:21: stderr=subprocess.PIPE,
.venv\Lib\site-packages\pygame\tests\docs_test.py:20: subprocess.run(
.venv\Lib\site-packages\pygame\tests\docs_test.py:26: stdout=subprocess.PIPE,
.venv\Lib\site-packages\pygame\tests\docs_test.py:27: stderr=subprocess.PIPE,
.venv\Lib\site-packages\pygame\tests\docs_test.py:29: except subprocess.TimeoutExpired:
.venv\Lib\site-packages\pygame\tests\test_utils\async_sub.py:101: PIPE = subprocess.PIPE
.venv\Lib\site-packages\pygame\tests\test_utils\async_sub.py:106: class Popen(subprocess.Popen):
.venv\Lib\site-packages\pygame\tests\test_utils\async_sub.py:175: except (subprocess.pywintypes.error, Exception):
.venv\Lib\site-packages\pygame\tests\test_utils\async_sub.py:196: except (subprocess.pywintypes.error, Exception):
.venv\Lib\site-packages\pygame\tests\test_utils\async_sub.py:260: stdin=subprocess.PIPE,
.venv\Lib\site-packages\pygame\tests\test_utils\async_sub.py:261: stdout=subprocess.PIPE,
.venv\Lib\site-packages\pygame\tests\test_utils\async_sub.py:262: stderr=subprocess.STDOUT,
.venv\Lib\site-packages\PySide6\QtAsyncio\events.py:636: stdin=subprocess.PIPE,
.venv\Lib\site-packages\PySide6\QtAsyncio\events.py:637: stdout=subprocess.PIPE,
.venv\Lib\site-packages\PySide6\QtAsyncio\events.py:638: stderr=subprocess.PIPE,
.venv\Lib\site-packages\PySide6\QtAsyncio\events.py:643: stdin=subprocess.PIPE,
.venv\Lib\site-packages\PySide6\QtAsyncio\events.py:644: stdout=subprocess.PIPE,
.venv\Lib\site-packages\PySide6\QtAsyncio\events.py:645: stderr=subprocess.PIPE,
.venv\Lib\site-packages\PySide6\scripts\pyside_tool.py:38: sys.exit(subprocess.call(command))
.venv\Lib\site-packages\PySide6\scripts\pyside_tool.py:51: returncode = subprocess.call(cmd)
.venv\Lib\site-packages\PySide6\scripts\pyside_tool.py:62: sys.exit(subprocess.call(command))
.venv\Lib\site-packages\PySide6\scripts\pyside_tool.py:146: subprocess.call(['xattr', '-dr', 'com.apple.provenance', os.fspath(temp_app)],
.venv\Lib\site-packages\PySide6\scripts\pyside_tool.py:147: stderr=subprocess.DEVNULL)
.venv\Lib\site-packages\PySide6\scripts\pyside_tool.py:153: subprocess.call(['codesign', '--force', '--deep', '--sign', '-',
.venv\Lib\site-packages\PySide6\scripts\pyside_tool.py:154: os.fspath(temp_app)], stderr=subprocess.DEVNULL)
.venv\Lib\site-packages\PySide6\scripts\pyside_tool.py:207: has_provenance = subprocess.call(
.venv\Lib\site-packages\PySide6\scripts\pyside_tool.py:209: stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0
.venv\Lib\site-packages\PySide6\scripts\pyside_tool.py:218: returncode = subprocess.call(cmd)
.venv\Lib\site-packages\PySide6\scripts\pyside_tool.py:241: sys.exit(subprocess.call(command))
.venv\Lib\site-packages\PySide6\scripts\deploy_lib\commands.py:25: output = subprocess.check_output(command, shell=is_windows)
.venv\Lib\site-packages\PySide6\scripts\deploy_lib\commands.py:27: subprocess.check_call(command, shell=is_windows)
.venv\Lib\site-packages\PySide6\scripts\deploy_lib\commands.py:32: except subprocess.CalledProcessError as error:
.venv\Lib\site-packages\PySide6\scripts\project_lib\project_data.py:243: with subprocess.Popen(cmd, stdout=subprocess.PIPE) as proc:
.venv\Lib\site-packages\PySide6\scripts\project_lib\utils.py:18: Run a command using a subprocess.
.venv\Lib\site-packages\PySide6\scripts\project_lib\utils.py:33: ex = subprocess.call(command, cwd=cwd)
.venv\Lib\site-packages\PySide6\scripts\project_lib\utils.py:103: output = subprocess.check_output([QTPATHS_CMD, "--query"])
core\tray.py:127: startupinfo = subprocess.STARTUPINFO()
core\tray.py:128: startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
core\tray.py:129: startupinfo.wShowWindow = subprocess.SW_HIDE
core\tray.py:131: proc = subprocess.Popen(
core\tray.py:139: stdin=subprocess.PIPE,
core\tray.py:140: stdout=subprocess.DEVNULL,
core\tray.py:141: stderr=subprocess.DEVNULL,
core\tray.py:143: creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0,
```

### Pattern: os\.system\s*\(

```text
.venv\Lib\site-packages\PIL\ImageShow.py:120: os.system(self.get_command(path, **options))  # nosec
```

### Pattern: eval\s*\(

```text
.venv\Lib\site-packages\numpy\f2py\auxfuncs.py:632: return eval(f"{l1}:{' and '.join(l2)}")
.venv\Lib\site-packages\numpy\f2py\auxfuncs.py:640: return eval(f"{l1}:{' or '.join(l2)}")
.venv\Lib\site-packages\numpy\f2py\auxfuncs.py:644: return eval('lambda v,f=f:not f(v)')
.venv\Lib\site-packages\numpy\f2py\capi_maps.py:159: d = eval(f.read().lower(), {}, {})
.venv\Lib\site-packages\numpy\f2py\capi_maps.py:299: ret['size'] = repr(eval(ret['size']))
.venv\Lib\site-packages\numpy\f2py\capi_maps.py:447: v = eval(v, {}, {})
.venv\Lib\site-packages\numpy\f2py\crackfortran.py:1325: v = eval(initexpr, {}, params)
.venv\Lib\site-packages\numpy\f2py\crackfortran.py:2272: def myeval(e, g=None, l=None):
.venv\Lib\site-packages\numpy\f2py\crackfortran.py:2274: r = eval(e, g, l)
.venv\Lib\site-packages\numpy\f2py\crackfortran.py:2305: c = int(myeval(e, {}, {}))
.venv\Lib\site-packages\numpy\f2py\crackfortran.py:2326: b = myeval(ee, {}, {})
.venv\Lib\site-packages\numpy\f2py\crackfortran.py:2331: a = myeval(ee, {}, {}) - b
.venv\Lib\site-packages\numpy\f2py\crackfortran.py:2336: c = myeval(ee, {}, {})
.venv\Lib\site-packages\numpy\f2py\crackfortran.py:2342: c2 = myeval(ee, {}, {})
.venv\Lib\site-packages\numpy\f2py\crackfortran.py:2532: params[n] = param_eval(v, g_params, params, dimspec=dimspec)
.venv\Lib\site-packages\numpy\f2py\crackfortran.py:2562: value = eval(value, {}, params)
.venv\Lib\site-packages\numpy\f2py\crackfortran.py:2639: l = str(eval(l, {}, params))
.venv\Lib\site-packages\numpy\f2py\crackfortran.py:2648: l = str(eval(l, {}, params))
.venv\Lib\site-packages\numpy\f2py\crackfortran.py:2916: kindselect['kind'] = eval(
.venv\Lib\site-packages\numpy\f2py\crackfortran.py:2966: def param_eval(v, g_params, params, dimspec=None):
.venv\Lib\site-packages\numpy\f2py\crackfortran.py:2987: p = eval(v, g_params, params)
.venv\Lib\site-packages\numpy\f2py\crackfortran.py:3018: item = eval(item, g_params, params)
.venv\Lib\site-packages\numpy\f2py\crackfortran.py:3470: v = eval(v)
.venv\Lib\site-packages\numpy\f2py\tests\test_crackfortran.py:267: class TestEval(util.F2PyTest):
.venv\Lib\site-packages\numpy\f2py\tests\test_crackfortran.py:378: ret = crackfortran.param_eval(v, g_params, params, dimspec=dimspec)
.venv\Lib\site-packages\numpy\f2py\tests\test_crackfortran.py:388: ret = crackfortran.param_eval(v, g_params, params, dimspec=dimspec)
.venv\Lib\site-packages\numpy\f2py\tests\test_crackfortran.py:407: ret = crackfortran.param_eval(v, g_params, params, dimspec=None)
.venv\Lib\site-packages\numpy\lib\_format_impl.py:536: See :py:func:`ast.literal_eval()` for details.
.venv\Lib\site-packages\numpy\lib\_format_impl.py:563: See :py:func:`ast.literal_eval()` for details.
.venv\Lib\site-packages\numpy\lib\_format_impl.py:658: d = ast.literal_eval(header)
.venv\Lib\site-packages\numpy\lib\_format_impl.py:663: d = ast.literal_eval(header)
.venv\Lib\site-packages\numpy\lib\_format_impl.py:799: See :py:func:`ast.literal_eval()` for details.
.venv\Lib\site-packages\numpy\lib\_format_impl.py:929: See :py:func:`ast.literal_eval()` for details.
.venv\Lib\site-packages\numpy\lib\_npyio_impl.py:151: See :py:func:`ast.literal_eval()` for details.
.venv\Lib\site-packages\numpy\lib\_npyio_impl.py:356: See :py:func:`ast.literal_eval()` for details.
.venv\Lib\site-packages\numpy\polynomial\hermite_e.py:245: >>> hermeval(0,hermeline(3, 2))
.venv\Lib\site-packages\numpy\polynomial\hermite_e.py:247: >>> hermeval(1,hermeline(3, 2))
.venv\Lib\site-packages\numpy\polynomial\hermite_e.py:303: >>> hermeval((-1, 0, 1), coef)
.venv\Lib\site-packages\numpy\polynomial\hermite_e.py:306: >>> hermeval((-1j, 1j), coef)
.venv\Lib\site-packages\numpy\polynomial\hermite_e.py:790: tmp[0] += k[i] - hermeval(lbnd, tmp)
.venv\Lib\site-packages\numpy\polynomial\hermite_e.py:796: def hermeval(x, c, tensor=True):
.venv\Lib\site-packages\numpy\polynomial\hermite_e.py:856: >>> hermeval(1, coef)
.venv\Lib\site-packages\numpy\polynomial\hermite_e.py:858: >>> hermeval([[1,2],[3,4]], coef)
.venv\Lib\site-packages\numpy\polynomial\hermite_e.py:1138: ``hermeval(x, c)`` are the same up to roundoff. This equivalence is
.venv\Lib\site-packages\numpy\polynomial\hermite_e.py:1407: >>> y = hermeval(x, [1, 2, 3]) + err
.venv\Lib\site-packages\numpy\polynomial\tests\test_hermite_e.py:79: val1 = herme.hermeval(self.x, pol1)
.venv\Lib\site-packages\numpy\polynomial\tests\test_hermite_e.py:83: val2 = herme.hermeval(self.x, pol2)
.venv\Lib\site-packages\numpy\polynomial\tests\test_hermite_e.py:85: val3 = herme.hermeval(self.x, pol3)
.venv\Lib\site-packages\numpy\polynomial\tests\test_hermite_e.py:120: def test_hermeval(self):
.venv\Lib\site-packages\numpy\polynomial\tests\test_hermite_e.py:122: assert_equal(herme.hermeval([], [1]).size, 0)
.venv\Lib\site-packages\numpy\polynomial\tests\test_hermite_e.py:130: res = herme.hermeval(x, [0] * i + [1])
.venv\Lib\site-packages\numpy\polynomial\tests\test_hermite_e.py:137: assert_equal(herme.hermeval(x, [1]).shape, dims)
.venv\Lib\site-packages\numpy\polynomial\tests\test_hermite_e.py:138: assert_equal(herme.hermeval(x, [1, 0]).shape, dims)
.venv\Lib\site-packages\numpy\polynomial\tests\test_hermite_e.py:139: assert_equal(herme.hermeval(x, [1, 0, 0]).shape, dims)
.venv\Lib\site-packages\numpy\polynomial\tests\test_hermite_e.py:258: assert_almost_equal(herme.hermeval(-1, hermeint), i)
.venv\Lib\site-packages\numpy\polynomial\tests\test_hermite_e.py:379: assert_almost_equal(v[..., i], herme.hermeval(x, coef))
.venv\Lib\site-packages\numpy\polynomial\tests\test_hermite_e.py:387: assert_almost_equal(v[..., i], herme.hermeval(x, coef))
.venv\Lib\site-packages\numpy\polynomial\tests\test_hermite_e.py:444: assert_almost_equal(herme.hermeval(x, coef3), y)
.venv\Lib\site-packages\numpy\polynomial\tests\test_hermite_e.py:447: assert_almost_equal(herme.hermeval(x, coef3), y)
.venv\Lib\site-packages\numpy\polynomial\tests\test_hermite_e.py:451: assert_almost_equal(herme.hermeval(x, coef4), y)
.venv\Lib\site-packages\numpy\polynomial\tests\test_hermite_e.py:454: assert_almost_equal(herme.hermeval(x, coef4), y)
.venv\Lib\site-packages\numpy\polynomial\tests\test_hermite_e.py:458: assert_almost_equal(herme.hermeval(x, coef4), y)
.venv\Lib\site-packages\numpy\polynomial\tests\test_hermite_e.py:487: assert_almost_equal(herme.hermeval(x, coef1), y)
.venv\Lib\site-packages\numpy\polynomial\tests\test_hermite_e.py:489: assert_almost_equal(herme.hermeval(x, coef2), y)
.venv\Lib\site-packages\numpy\polynomial\tests\test_hermite_e.py:535: res = herme.hermeval(roots, pol)
.venv\Lib\site-packages\numpy\tests\test_public_api.py:322: eval(module_name)
.venv\Lib\site-packages\numpy\_core\arrayprint.py:1577: >>> assert eval(dtype_short_repr(dt)) == dt
.venv\Lib\site-packages\numpy\_core\_internal.py:204: newitem = (dtype, ast.literal_eval(repeats))
.venv\Lib\site-packages\numpy\_core\tests\test_arrayprint.py:343: assert_equal(eval(repr(a), vars(np)), a)
.venv\Lib\site-packages\numpy\_core\tests\test_arrayprint.py:344: assert_equal(eval(repr(a[0]), {'np': np}), a[0])
.venv\Lib\site-packages\numpy\_core\tests\test_dtype.py:996: assert_equal(np.dtype(eval(str(dt))), dt)
.venv\Lib\site-packages\numpy\_core\tests\test_multiarray.py:1703: assert_array_equal(eval(repr(xx), {"np": np, "array": np.array}), xx)
.venv\Lib\site-packages\numpy\_core\tests\test_records.py:185: recarr_r = eval("np." + repr(recarr), {'np': np})
.venv\Lib\site-packages\numpy\_core\tests\test_records.py:187: recordview_r = eval("np." + repr(recordview), {'np': np, 'numpy': np})
.venv\Lib\site-packages\numpy\_core\tests\test_scalarmath.py:610: #            val2 = eval(val_repr)
.venv\Lib\site-packages\numpy\_core\tests\test_scalarmath.py:636: val2 = t(eval(val_repr))
.venv\Lib\site-packages\numpy\_core\tests\test_simd.py:244: func = eval(intrin)
.venv\Lib\site-packages\numpy\_core\tests\test_simd.py:512: func = eval(intrin[:3])
.venv\Lib\site-packages\numpy\_core\tests\test_simd.py:642: func = eval(intrin)
.venv\Lib\site-packages\numpy\_core\tests\test_simd.py:703: npyv_load_tillz, npyv_load_till = eval(intrin)
.venv\Lib\site-packages\numpy\_core\tests\test_simd.py:723: npyv_store_till = eval(intrin)
.venv\Lib\site-packages\numpy\_core\tests\test_simd.py:743: npyv_loadn = eval(intrin)
.venv\Lib\site-packages\numpy\_core\tests\test_simd.py:769: npyv_loadn_tillz, npyv_loadn_till = eval(intrin)
.venv\Lib\site-packages\numpy\_core\tests\test_simd.py:806: npyv_storen = eval(intrin)
.venv\Lib\site-packages\numpy\_core\tests\test_simd.py:845: npyv_storen_till = eval(intrin)
.venv\Lib\site-packages\numpy\_core\tests\test_simd.py:897: intrin = eval(intrin)
.venv\Lib\site-packages\numpy\_core\tests\test_simd.py:1104: func = eval(intrin)
.venv\Lib\site-packages\numpy\_core\tests\test_umath.py:513: a, b, divisors = eval(ex_val)
.venv\Lib\site-packages\numpy\_core\tests\test_umath.py:576: a = eval(ex_val)
.venv\Lib\site-packages\numpy\_core\tests\test_umath_accuracy.py:75: dtype=eval(datatype))
.venv\Lib\site-packages\numpy\_core\tests\test_umath_accuracy.py:78: dtype=eval(datatype))
.venv\Lib\site-packages\PIL\GifImagePlugin.py:736: mask = ImageMath.lambda_eval(
.venv\Lib\site-packages\PIL\GifImagePlugin.py:758: mask = ImageMath.lambda_eval(
.venv\Lib\site-packages\PIL\Image.py:3776: def eval(image: Image, *args: Callable[[int], float]) -> Image:
.venv\Lib\site-packages\PIL\ImageMath.py:239: def lambda_eval(expression: Callable[[dict[str, Any]], Any], **kw: Any) -> Any:
.venv\Lib\site-packages\PIL\ImageMath.py:267: def unsafe_eval(expression: str, **kw: Any) -> Any:
.venv\Lib\site-packages\PIL\ImageMath.py:269: Evaluates an image expression. This uses Python's ``eval()`` function to process
.venv\Lib\site-packages\PIL\ImageMath.py:310: out = builtins.eval(expression, None, args)
.venv\Lib\site-packages\pip\_vendor\packaging\_parser.py:372: value = ast.literal_eval(python_str)
.venv\Lib\site-packages\pip\_vendor\pygments\formatters\__init__.py:91: this method is equivalent to running ``eval()`` on the input file. The formatter is
.venv\Lib\site-packages\pip\_vendor\rich\markup.py:190: meta_params = literal_eval(parameters)
.venv\Lib\site-packages\pygame\tests\test_utils\run_tests.py:52: dump - dump failures/errors as dict ready to eval (default False)
.venv\Lib\site-packages\pygame\tests\test_utils\test_runner.py:245: return eval(test_results.group(1))
```

### Pattern: exec\s*\(

```text
main.py:345: return app.exec()
.venv\Lib\site-packages\numpy\f2py\tests\test_f2py2e.py:889: def test_npd_f77exec():
.venv\Lib\site-packages\numpy\f2py\tests\test_f2py2e.py:897: def test_npd_f90exec():
.venv\Lib\site-packages\numpy\testing\_private\utils.py:1352: exec(astr, dict)
.venv\Lib\site-packages\numpy\testing\_private\utils.py:1640: exec(code, globs, locs)
.venv\Lib\site-packages\pip\_vendor\distlib\scripts.py:165: # shebang, or else using os.exec() to run the entry script will
.venv\Lib\site-packages\pip\_vendor\pkg_resources\__init__.py:1714: exec(code, namespace, namespace)
.venv\Lib\site-packages\pip\_vendor\pkg_resources\__init__.py:1725: exec(script_code, namespace, namespace)
.venv\Lib\site-packages\pip\_vendor\pygments\formatters\__init__.py:103: exec(f.read(), custom_namespace)
.venv\Lib\site-packages\pip\_vendor\pygments\lexers\__init__.py:154: exec(f.read(), custom_namespace)
.venv\Lib\site-packages\PySide6\QtAsyncio\events.py:89: self._loop.exec()
.venv\Lib\site-packages\PySide6\QtAsyncio\events.py:276: self._application.exec()
.venv\Lib\site-packages\PySide6\QtAsyncio\events.py:635: async def subprocess_exec(self, protocol_factory, *args,
.venv\Lib\site-packages\PySide6\QtAsyncio\events.py:640: raise NotImplementedError("QAsyncioEventLoop.subprocess_exec() is not implemented yet")
.venv\Lib\site-packages\PySide6\scripts\qml.py:246: exit_code = app.exec()
.venv\Lib\site-packages\PySide6\scripts\project_lib\newproject.py:20: sys.exit(app.exec())
.venv\Lib\site-packages\PySide6\scripts\project_lib\newproject.py:93: exit_code = app.exec()
ui\main_window.py:109: sys.exit(app.exec())
ui\main_window_ui.py:269: dialog.exec()
ui\main_window_ui.py:274: dialog.exec()
```

### Pattern: pickle\.

```text
.venv\Lib\site-packages\numpy\core\_internal.py:4: # Build a new array from the information in a pickle.
.venv\Lib\site-packages\numpy\core\__init__.py:11: # We used to use `np.core._ufunc_reconstruct` to unpickle.
.venv\Lib\site-packages\numpy\lib\_format_impl.py:724: Additional keyword arguments to pass to pickle.dump, excluding
.venv\Lib\site-packages\numpy\lib\_format_impl.py:762: pickle.dump(array, fp, protocol=4, **pickle_kwargs)
.venv\Lib\site-packages\numpy\lib\_format_impl.py:794: Additional keyword arguments to pass to pickle.load. These are only
.venv\Lib\site-packages\numpy\lib\_format_impl.py:838: array = pickle.load(fp, **pickle_kwargs)
.venv\Lib\site-packages\numpy\lib\_npyio_impl.py:145: Additional keyword arguments to pass on to pickle.load.
.venv\Lib\site-packages\numpy\lib\_npyio_impl.py:371: If ``allow_pickle=True``, but the file cannot be loaded as a pickle.
.venv\Lib\site-packages\numpy\lib\_npyio_impl.py:492: "`allow_pickle=` keyword argument or `pickle.load()`.")
.venv\Lib\site-packages\numpy\lib\_npyio_impl.py:494: return pickle.load(fid, **pickle_kwargs)
.venv\Lib\site-packages\numpy\lib\_npyio_impl.py:496: raise pickle.UnpicklingError(
.venv\Lib\site-packages\numpy\ma\core.py:6542: information stored in a pickle.
.venv\Lib\site-packages\numpy\ma\mrecords.py:455: Build a new MaskedArray from the information stored in a pickle.
.venv\Lib\site-packages\numpy\ma\tests\test_core.py:728: for proto in range(2, pickle.HIGHEST_PROTOCOL + 1):
.venv\Lib\site-packages\numpy\ma\tests\test_core.py:731: a_pickled = pickle.loads(pickle.dumps(a, protocol=proto))
.venv\Lib\site-packages\numpy\ma\tests\test_core.py:745: for proto in range(2, pickle.HIGHEST_PROTOCOL + 1):
.venv\Lib\site-packages\numpy\ma\tests\test_core.py:746: a_pickled = pickle.loads(pickle.dumps(a, protocol=proto))
.venv\Lib\site-packages\numpy\ma\tests\test_core.py:754: for proto in range(2, pickle.HIGHEST_PROTOCOL + 1):
.venv\Lib\site-packages\numpy\ma\tests\test_core.py:755: mc_pickled = pickle.loads(pickle.dumps(mc, protocol=proto))
.venv\Lib\site-packages\numpy\ma\tests\test_core.py:764: for proto in range(2, pickle.HIGHEST_PROTOCOL + 1):
.venv\Lib\site-packages\numpy\ma\tests\test_core.py:765: a_pickled = pickle.loads(pickle.dumps(a, protocol=proto))
.venv\Lib\site-packages\numpy\ma\tests\test_core.py:773: for proto in range(2, pickle.HIGHEST_PROTOCOL + 1):
.venv\Lib\site-packages\numpy\ma\tests\test_core.py:774: test = pickle.loads(pickle.dumps(b, protocol=proto))
.venv\Lib\site-packages\numpy\ma\tests\test_core.py:5677: for proto in range(2, pickle.HIGHEST_PROTOCOL + 1):
.venv\Lib\site-packages\numpy\ma\tests\test_core.py:5679: pickle.dump(np.ma.masked, f, protocol=proto)
.venv\Lib\site-packages\numpy\ma\tests\test_core.py:5681: res = pickle.load(f)
.venv\Lib\site-packages\numpy\ma\tests\test_mrecords.py:289: for proto in range(2, pickle.HIGHEST_PROTOCOL + 1):
.venv\Lib\site-packages\numpy\ma\tests\test_mrecords.py:290: _ = pickle.dumps(mrec, protocol=proto)
.venv\Lib\site-packages\numpy\ma\tests\test_mrecords.py:291: mrec_ = pickle.loads(_)
.venv\Lib\site-packages\numpy\ma\tests\test_old_ma.py:615: for proto in range(2, pickle.HIGHEST_PROTOCOL + 1):
.venv\Lib\site-packages\numpy\ma\tests\test_old_ma.py:616: s = pickle.dumps(x, protocol=proto)
.venv\Lib\site-packages\numpy\ma\tests\test_old_ma.py:617: y = pickle.loads(s)
.venv\Lib\site-packages\numpy\matrixlib\tests\test_masked_matrix.py:88: for proto in range(2, pickle.HIGHEST_PROTOCOL + 1):
.venv\Lib\site-packages\numpy\matrixlib\tests\test_masked_matrix.py:89: a_pickled = pickle.loads(pickle.dumps(a, protocol=proto))
.venv\Lib\site-packages\numpy\polynomial\tests\test_polynomial.py:62: y = pickle.loads(pickle.dumps(x))
.venv\Lib\site-packages\numpy\random\tests\test_direct.py:327: bitgen_pkl = pickle.dumps(bit_generator)
.venv\Lib\site-packages\numpy\random\tests\test_direct.py:328: reloaded = pickle.loads(bitgen_pkl)
.venv\Lib\site-packages\numpy\random\tests\test_direct.py:336: aa = pickle.loads(pickle.dumps(ss))
.venv\Lib\site-packages\numpy\random\tests\test_direct.py:346: bg_plk = pickle.loads(pickle.dumps(bit_generator))
.venv\Lib\site-packages\numpy\random\tests\test_direct.py:352: bg_plk = pickle.loads(pickle.dumps(bit_generator))
.venv\Lib\site-packages\numpy\random\tests\test_direct.py:580: sfc = pickle.load(gz)
.venv\Lib\site-packages\numpy\random\tests\test_generator_mt19937.py:2802: rg_plk = pickle.loads(pickle.dumps(rg))
.venv\Lib\site-packages\numpy\random\tests\test_generator_mt19937.py:2808: rg_plk = pickle.loads(pickle.dumps(rg))
.venv\Lib\site-packages\numpy\random\tests\test_generator_mt19937.py:2824: rg = pickle.load(gz)
.venv\Lib\site-packages\numpy\random\tests\test_randomstate.py:272: rs_unpick = pickle.loads(pickle.dumps(random_state))
.venv\Lib\site-packages\numpy\random\tests\test_smoke.py:487: pick = pickle.dumps(rg)
.venv\Lib\site-packages\numpy\random\tests\test_smoke.py:488: unpick = pickle.loads(pick)
.venv\Lib\site-packages\numpy\random\tests\test_smoke.py:493: pick = pickle.dumps(rg)
.venv\Lib\site-packages\numpy\random\tests\test_smoke.py:494: unpick = pickle.loads(pick)
.venv\Lib\site-packages\numpy\tests\test_reloading.py:38: for proto in range(2, pickle.HIGHEST_PROTOCOL + 1):
.venv\Lib\site-packages\numpy\tests\test_reloading.py:40: assert_(pickle.loads(pickle.dumps(np._NoValue,
.venv\Lib\site-packages\numpy\_core\records.py:703: >>> pickle.loads(pickle.dumps(r))
.venv\Lib\site-packages\numpy\_core\_add_newdocs.py:1980: Construct an empty array. Used by Pickle.
.venv\Lib\site-packages\numpy\_core\_add_newdocs.py:3818: The array can be read back with pickle.load or numpy.load.
.venv\Lib\site-packages\numpy\_core\_add_newdocs.py:3831: ``pickle.loads`` will convert the string back to an array.
.venv\Lib\site-packages\numpy\_core\_methods.py:244: pickle.dump(self, f, protocol=protocol)
.venv\Lib\site-packages\numpy\_core\_methods.py:247: return pickle.dumps(self, protocol=protocol)
.venv\Lib\site-packages\numpy\_core\tests\test_custom_dtypes.py:503: s = pickle.dumps(SF)
.venv\Lib\site-packages\numpy\_core\tests\test_custom_dtypes.py:504: res = pickle.loads(s)
.venv\Lib\site-packages\numpy\_core\tests\test_datetime.py:910: for proto in range(2, pickle.HIGHEST_PROTOCOL + 1):
.venv\Lib\site-packages\numpy\_core\tests\test_datetime.py:912: assert_equal(pickle.loads(pickle.dumps(dt, protocol=proto)), dt)
.venv\Lib\site-packages\numpy\_core\tests\test_datetime.py:914: assert_equal(pickle.loads(pickle.dumps(dt, protocol=proto)), dt)
.venv\Lib\site-packages\numpy\_core\tests\test_datetime.py:916: assert_equal(pickle.loads(pickle.dumps(scalar, protocol=proto)),
.venv\Lib\site-packages\numpy\_core\tests\test_datetime.py:919: assert_equal(pickle.loads(pickle.dumps(delta, protocol=proto)),
.venv\Lib\site-packages\numpy\_core\tests\test_datetime.py:926: assert_equal(pickle.loads(pkl), np.dtype('<M8[7D]'))
.venv\Lib\site-packages\numpy\_core\tests\test_datetime.py:930: assert_equal(pickle.loads(pkl), np.dtype('<M8[W]'))
.venv\Lib\site-packages\numpy\_core\tests\test_datetime.py:934: assert_equal(pickle.loads(pkl), np.dtype('>M8[us]'))
.venv\Lib\site-packages\numpy\_core\tests\test_datetime.py:940: for proto in range(2, pickle.HIGHEST_PROTOCOL + 1):
.venv\Lib\site-packages\numpy\_core\tests\test_datetime.py:941: res = pickle.loads(pickle.dumps(dt, protocol=proto))
.venv\Lib\site-packages\numpy\_core\tests\test_dtype.py:1295: for proto in range(pickle.HIGHEST_PROTOCOL + 1):
.venv\Lib\site-packages\numpy\_core\tests\test_dtype.py:1296: buf = pickle.dumps(dtype, proto)
.venv\Lib\site-packages\numpy\_core\tests\test_dtype.py:1301: pickled = pickle.loads(buf)
.venv\Lib\site-packages\numpy\_core\tests\test_dtype.py:1371: for proto in range(pickle.HIGHEST_PROTOCOL + 1):
.venv\Lib\site-packages\numpy\_core\tests\test_dtype.py:1372: roundtrip_DType = pickle.loads(pickle.dumps(DType, proto))
.venv\Lib\site-packages\numpy\_core\tests\test_dtype.py:1382: for proto in range(pickle.HIGHEST_PROTOCOL + 1):
.venv\Lib\site-packages\numpy\_core\tests\test_dtype.py:1383: roundtrip_dt = pickle.loads(pickle.dumps(dt, proto))
.venv\Lib\site-packages\numpy\_core\tests\test_multiarray.py:192: for v in range(pickle.HIGHEST_PROTOCOL):
.venv\Lib\site-packages\numpy\_core\tests\test_multiarray.py:193: vals = pickle.loads(pickle.dumps(a, v))
.venv\Lib\site-packages\numpy\_core\tests\test_multiarray.py:1855: scalar = pickle.loads(pickle.dumps(scalar))
.venv\Lib\site-packages\numpy\_core\tests\test_multiarray.py:2007: assert_equal(zs, pickle.loads(zs.dumps()))
.venv\Lib\site-packages\numpy\_core\tests\test_multiarray.py:2010: for proto in range(2, pickle.HIGHEST_PROTOCOL + 1):
.venv\Lib\site-packages\numpy\_core\tests\test_multiarray.py:2013: p = pickle.dumps(zs, protocol=proto)
.venv\Lib\site-packages\numpy\_core\tests\test_multiarray.py:2014: zs2 = pickle.loads(p)
.venv\Lib\site-packages\numpy\_core\tests\test_multiarray.py:2022: pk_dmp = pickle.dumps(arr)
.venv\Lib\site-packages\numpy\_core\tests\test_multiarray.py:2023: pk_load = pickle.loads(pk_dmp)
.venv\Lib\site-packages\numpy\_core\tests\test_multiarray.py:2027: @pytest.mark.skipif(pickle.HIGHEST_PROTOCOL < 5,
.venv\Lib\site-packages\numpy\_core\tests\test_multiarray.py:2032: bytes_string = pickle.dumps(array, buffer_callback=buffers.append,
.venv\Lib\site-packages\numpy\_core\tests\test_multiarray.py:2034: array_from_buffer = pickle.loads(bytes_string, buffers=buffers)
.venv\Lib\site-packages\numpy\_core\tests\test_multiarray.py:4932: pickle.HIGHEST_PROTOCOL >= 5,
.venv\Lib\site-packages\numpy\_core\tests\test_multiarray.py:4951: for proto in range(2, pickle.HIGHEST_PROTOCOL + 1):
.venv\Lib\site-packages\numpy\_core\tests\test_multiarray.py:4952: depickled_arr_with_object = pickle.loads(
.venv\Lib\site-packages\numpy\_core\tests\test_multiarray.py:4953: pickle.dumps(arr_with_object, protocol=proto))
.venv\Lib\site-packages\numpy\_core\tests\test_multiarray.py:4954: depickled_arr_without_object = pickle.loads(
.venv\Lib\site-packages\numpy\_core\tests\test_multiarray.py:4955: pickle.dumps(arr_without_object, protocol=proto))
.venv\Lib\site-packages\numpy\_core\tests\test_multiarray.py:4963: pickle.HIGHEST_PROTOCOL < 5,
.venv\Lib\site-packages\numpy\_core\tests\test_multiarray.py:4972: bytes_string = pickle.dumps(f_contiguous_array, protocol=5,
.venv\Lib\site-packages\numpy\_core\tests\test_multiarray.py:4977: depickled_f_contiguous_array = pickle.loads(bytes_string,
.venv\Lib\site-packages\numpy\_core\tests\test_multiarray.py:4983: pickle.HIGHEST_PROTOCOL < 5,
.venv\Lib\site-packages\numpy\_core\tests\test_multiarray.py:5003: bytes_string = pickle.dumps(transposed_contiguous_array, protocol=5,
.venv\Lib\site-packages\numpy\_core\tests\test_multiarray.py:5008: depickled_transposed_contiguous_array = pickle.loads(bytes_string,
.venv\Lib\site-packages\numpy\_core\tests\test_multiarray.py:5014: pickle.HIGHEST_PROTOCOL < 5,
.venv\Lib\site-packages\numpy\_core\tests\test_multiarray.py:5024: assert_equal(x, pickle.loads(c_contiguous_dumped))
.venv\Lib\site-packages\numpy\_core\tests\test_multiarray.py:5026: assert_equal(x, pickle.loads(f_contiguous_dumped))
.venv\Lib\site-packages\numpy\_core\tests\test_multiarray.py:5028: assert_equal(x, pickle.loads(transposed_contiguous_dumped))
.venv\Lib\site-packages\numpy\_core\tests\test_multiarray.py:5030: assert_equal(x, pickle.loads(no_contiguous_dumped))
.venv\Lib\site-packages\numpy\_core\tests\test_multiarray.py:5040: for proto in range(2, pickle.HIGHEST_PROTOCOL + 1):
.venv\Lib\site-packages\numpy\_core\tests\test_multiarray.py:5042: depickled_non_contiguous_array = pickle.loads(
.venv\Lib\site-packages\numpy\_core\tests\test_multiarray.py:5043: pickle.dumps(
.venv\Lib\site-packages\numpy\_core\tests\test_multiarray.py:5055: for proto in range(2, pickle.HIGHEST_PROTOCOL + 1):
.venv\Lib\site-packages\numpy\_core\tests\test_multiarray.py:5067: a, pickle.loads(pickle.dumps(a, protocol=proto)),
.venv\Lib\site-packages\numpy\_core\tests\test_multiarray.py:5076: return pickle.loads(obj, encoding='latin1')
.venv\Lib\site-packages\numpy\_core\tests\test_multiarray.py:5177: new = pickle.loads(pickle.dumps(original_byte_reversed))
.venv\Lib\site-packages\numpy\_core\tests\test_multiarray.py:9144: pickle_obj = pickle.dumps(obj)
.venv\Lib\site-packages\numpy\_core\tests\test_multiarray.py:9145: res = pickle.loads(pickle_obj)
.venv\Lib\site-packages\numpy\_core\tests\test_overrides.py:220: for proto in range(2, pickle.HIGHEST_PROTOCOL + 1):
.venv\Lib\site-packages\numpy\_core\tests\test_overrides.py:221: roundtripped = pickle.loads(
.venv\Lib\site-packages\numpy\_core\tests\test_overrides.py:222: pickle.dumps(dispatched_one_arg, protocol=proto))
.venv\Lib\site-packages\numpy\_core\tests\test_records.py:429: for proto in range(2, pickle.HIGHEST_PROTOCOL + 1):
.venv\Lib\site-packages\numpy\_core\tests\test_records.py:430: assert_equal(a, pickle.loads(pickle.dumps(a, protocol=proto)))
.venv\Lib\site-packages\numpy\_core\tests\test_records.py:431: assert_equal(a[0], pickle.loads(pickle.dumps(a[0],
.venv\Lib\site-packages\numpy\_core\tests\test_records.py:436: for proto in range(2, pickle.HIGHEST_PROTOCOL + 1):
.venv\Lib\site-packages\numpy\_core\tests\test_records.py:437: assert_equal(a, pickle.loads(pickle.dumps(a, protocol=proto)))
.venv\Lib\site-packages\numpy\_core\tests\test_records.py:438: assert_equal(a[0], pickle.loads(pickle.dumps(a[0],
.venv\Lib\site-packages\numpy\_core\tests\test_records.py:444: for proto in range(2, pickle.HIGHEST_PROTOCOL + 1):
.venv\Lib\site-packages\numpy\_core\tests\test_records.py:445: pa = pickle.loads(pickle.dumps(a[0], protocol=proto))
.venv\Lib\site-packages\numpy\_core\tests\test_records.py:468: dump = pickle.dumps(a[0])
.venv\Lib\site-packages\numpy\_core\tests\test_records.py:469: unpickled = pickle.loads(dump)
.venv\Lib\site-packages\numpy\_core\tests\test_regression.py:53: for proto in range(2, pickle.HIGHEST_PROTOCOL + 1):
.venv\Lib\site-packages\numpy\_core\tests\test_regression.py:55: pickle.dump(a, f, protocol=proto)
.venv\Lib\site-packages\numpy\_core\tests\test_regression.py:57: b = pickle.load(f)
.venv\Lib\site-packages\numpy\_core\tests\test_regression.py:103: for proto in range(2, pickle.HIGHEST_PROTOCOL + 1):
.venv\Lib\site-packages\numpy\_core\tests\test_regression.py:105: pickle.dump(ca, f, protocol=proto)
.venv\Lib\site-packages\numpy\_core\tests\test_regression.py:365: for proto in range(2, pickle.HIGHEST_PROTOCOL + 1):
.venv\Lib\site-packages\numpy\_core\tests\test_regression.py:367: pickle.dump(dt, f, protocol=proto)
.venv\Lib\site-packages\numpy\_core\tests\test_regression.py:369: dt_ = pickle.load(f)
.venv\Lib\site-packages\numpy\_core\tests\test_regression.py:495: result = pickle.loads(data, encoding='bytes')
.venv\Lib\site-packages\numpy\_core\tests\test_regression.py:504: for proto in range(2, pickle.HIGHEST_PROTOCOL + 1):
.venv\Lib\site-packages\numpy\_core\tests\test_regression.py:505: pickle.dumps(float, protocol=proto)
.venv\Lib\site-packages\numpy\_core\tests\test_regression.py:839: for proto in range(2, pickle.HIGHEST_PROTOCOL + 1):
.venv\Lib\site-packages\numpy\_core\tests\test_regression.py:840: new = pickle.loads(pickle.dumps(el, protocol=proto))
.venv\Lib\site-packages\numpy\_core\tests\test_regression.py:1075: for proto in range(2, pickle.HIGHEST_PROTOCOL + 1):
.venv\Lib\site-packages\numpy\_core\tests\test_regression.py:1076: y = pickle.loads(pickle.dumps(x, protocol=proto))
.venv\Lib\site-packages\numpy\_core\tests\test_regression.py:1092: xp = pickle.load(f, encoding='latin1')
.venv\Lib\site-packages\numpy\_core\tests\test_regression.py:1290: for proto in range(2, pickle.HIGHEST_PROTOCOL + 1):
.venv\Lib\site-packages\numpy\_core\tests\test_regression.py:1291: assert_(pickle.loads(
.venv\Lib\site-packages\numpy\_core\tests\test_regression.py:1292: pickle.dumps(test_string, protocol=proto)) == test_string)
.venv\Lib\site-packages\numpy\_core\tests\test_regression.py:1293: assert_(pickle.loads(
.venv\Lib\site-packages\numpy\_core\tests\test_regression.py:1294: pickle.dumps(test_record, protocol=proto)) == test_record)
.venv\Lib\site-packages\numpy\_core\tests\test_regression.py:1898: blob = pickle.dumps(data, protocol=1)
.venv\Lib\site-packages\numpy\_core\tests\test_regression.py:1899: data = pickle.loads(blob)
.venv\Lib\site-packages\numpy\_core\tests\test_regression.py:1909: for proto in range(2, pickle.HIGHEST_PROTOCOL + 1):
.venv\Lib\site-packages\numpy\_core\tests\test_regression.py:1911: data = pickle.loads(pickle.dumps(data, protocol=proto))
.venv\Lib\site-packages\numpy\_core\tests\test_regression.py:1924: # Python2 output for pickle.dumps(numpy.array([129], dtype='b'))
.venv\Lib\site-packages\numpy\_core\tests\test_regression.py:1932: result = pickle.loads(data, encoding='latin1')
.venv\Lib\site-packages\numpy\_core\tests\test_regression.py:1935: assert_raises(Exception, pickle.loads, data, encoding='koi8-r')
.venv\Lib\site-packages\numpy\_core\tests\test_regression.py:1944: # Python2 output for pickle.dumps(...)
.venv\Lib\site-packages\numpy\_core\tests\test_regression.py:1961: result = pickle.loads(data, encoding='latin1')
.venv\Lib\site-packages\numpy\_core\tests\test_regression.py:1970: result = pickle.loads(data, encoding='koi8-r')
.venv\Lib\site-packages\numpy\_core\tests\test_regression.py:1976: ValueError, pickle.loads, data, encoding='koi8-r'
.venv\Lib\site-packages\numpy\_core\tests\test_regression.py:2213: for proto in range(2, pickle.HIGHEST_PROTOCOL + 1):
.venv\Lib\site-packages\numpy\_core\tests\test_regression.py:2215: assert_equal(pickle.loads(
.venv\Lib\site-packages\numpy\_core\tests\test_regression.py:2216: pickle.dumps(test_string, protocol=proto)), test_string)
.venv\Lib\site-packages\numpy\_core\tests\test_regression.py:2400: range(2, pickle.HIGHEST_PROTOCOL + 1)
.venv\Lib\site-packages\numpy\_core\tests\test_regression.py:2404: s = pickle.dumps(val, protocol)
.venv\Lib\site-packages\numpy\_core\tests\test_regression.py:2433: for proto in range(2, pickle.HIGHEST_PROTOCOL + 1):
.venv\Lib\site-packages\numpy\_core\tests\test_regression.py:2434: dumped = pickle.dumps(arr, protocol=proto)
.venv\Lib\site-packages\numpy\_core\tests\test_regression.py:2435: assert_equal(pickle.loads(dumped), arr)
.venv\Lib\site-packages\numpy\_core\tests\test_regression.py:2569: result = pickle.loads(test_data, encoding='bytes')
.venv\Lib\site-packages\numpy\_core\tests\test_stringdtype.py:645: pickle.dump([arr, dtype], f)
.venv\Lib\site-packages\numpy\_core\tests\test_stringdtype.py:648: res = pickle.load(f)
.venv\Lib\site-packages\numpy\_core\tests\test_ufunc.py:202: for proto in range(2, pickle.HIGHEST_PROTOCOL + 1):
.venv\Lib\site-packages\numpy\_core\tests\test_ufunc.py:203: assert_(pickle.loads(pickle.dumps(np.sin,
.venv\Lib\site-packages\numpy\_core\tests\test_ufunc.py:208: res = pickle.loads(pickle.dumps(_rational_tests.test_add,
.venv\Lib\site-packages\numpy\_core\tests\test_ufunc.py:215: assert_(pickle.loads(astring) is np.cos)
.venv\Lib\site-packages\numpy\_core\tests\test_ufunc.py:224: obj = pickle.loads(pickle.dumps(_pickleable_module_global.ufunc))
.venv\Lib\site-packages\numpy\_core\tests\test_ufunc.py:499: int64_2 = pickle.loads(pickle.dumps(int64))
.venv\Lib\site-packages\numpy\_core\tests\test__exceptions.py:19: res = pickle.loads(pickle.dumps(error))
.venv\Lib\site-packages\numpy\_core\tests\test__exceptions.py:61: assert isinstance(pickle.dumps(_UFuncNoLoopError), bytes)
.venv\Lib\site-packages\numpy\_core\tests\test__exceptions.py:84: exc2 = pickle.loads(pickle.dumps(exc))
.venv\Lib\site-packages\pip\_vendor\msgpack\__init__.py:50: # alias for compatibility to simplejson/marshal/pickle.
.venv\Lib\site-packages\pip\_vendor\packaging\_structures.py:10: stand-in classes so that ``pickle.loads()`` can resolve those references.
.venv\Lib\site-packages\pygame\tests\color_test.py:1172: pickle_string = pickle.dumps(c1)
.venv\Lib\site-packages\pygame\tests\color_test.py:1173: c1_frompickle = pickle.loads(pickle_string)
.venv\Lib\site-packages\pygame\tests\math_test.py:2990: self.assertEqual(pickle.loads(pickle.dumps(v2)), v2)
.venv\Lib\site-packages\pygame\tests\math_test.py:2991: self.assertEqual(pickle.loads(pickle.dumps(v3)), v3)
```

### Pattern: yaml\.load\s*\(

```text
[No matches]
```

### Pattern: powershell\.exe

```text
core\tray.py:133: "powershell.exe",
```

### Pattern: Invoke-Expression

```text
[No matches]
```

### Pattern: Start-Process

```text
tests\test_phase1_p0.py:27: payload_malicioso_titulo = 'Prueba"; Start-Process calc.exe; #'
```

### Pattern: requests\.(get|post|put|patch|delete)\s*\(

```text
.venv\Lib\site-packages\pip\_vendor\requests\__init__.py:14: >>> r = requests.get('https://www.python.org')
.venv\Lib\site-packages\pip\_vendor\requests\__init__.py:23: >>> r = requests.post('https://httpbin.org/post', data=payload)
.venv\Lib\site-packages\requests\__init__.py:14: >>> r = requests.get('https://www.python.org')
.venv\Lib\site-packages\requests\__init__.py:23: >>> r = requests.post('https://httpbin.org/post', data=payload)
core\api.py:8: response = requests.get(API_URL, headers=API_HEADERS, timeout=10)
ui\main_window_games.py:52: response = requests.get(API_URL, headers=API_HEADERS, timeout=1.2)
ui\main_window_helpers.py:74: res = requests.get(url_img, headers=headers, timeout=5)

```text
.venv\Lib\site-packages\pygame\docs\serve.py:64: webbrowser.open(f"http://{TARGET}:{parsed_args.port}")
core\validators.py:79: webbrowser.open(url)
ui\main_window_helpers.py:101: webbrowser.open(url)

### Pattern: open\s*\([^)]*['"]w['"]

main.py:21: sys.stdout = open(os.devnull, "w", encoding="utf-8")
main.py:27: sys.stderr = open(os.devnull, "w", encoding="utf-8")
.venv\Lib\site-packages\numpy\f2py\crackfortran.py:3724: with open(pyffilename, 'w') as f:
.venv\Lib\site-packages\numpy\f2py\f2py2e.py:357: with open(options['signsfile'], 'w') as f:
.venv\Lib\site-packages\numpy\f2py\rules.py:1436: with open(fn, 'w') as f:
.venv\Lib\site-packages\numpy\f2py\rules.py:1443: with open(fn, 'w') as f:
.venv\Lib\site-packages\numpy\f2py\rules.py:1451: with open(fn, 'w') as f:
.venv\Lib\site-packages\numpy\f2py\rules.py:1464: with open(wn, 'w') as f:
.venv\Lib\site-packages\numpy\f2py\rules.py:1489: with open(wn, 'w') as f:
.venv\Lib\site-packages\numpy\f2py\tests\test_crackfortran.py:284: with f_path.open('w', encoding=encoding) as ff:
.venv\Lib\site-packages\numpy\f2py\tests\test_f2py2e.py:524: with open(fpath, "w") as f:
.venv\Lib\site-packages\numpy\f2py\tests\util.py:38: with open(meson_file, "w") as f:
.venv\Lib\site-packages\numpy\f2py\tests\util.py:290: with open(path, "w") as f:
.venv\Lib\site-packages\numpy\lib\_npyio_impl.py:785: with zipf.open(fname, 'w', force_zip64=True) as fid:
.venv\Lib\site-packages\numpy\lib\tests\test_io.py:219: with npz.open("test1.npy", "w") as out_file:
.venv\Lib\site-packages\numpy\lib\tests\test_io.py:221: with npz.open("test2", "w") as out_file:
.venv\Lib\site-packages\numpy\lib\tests\test_io.py:223: with npz.open("metadata", "w") as out_file:
.venv\Lib\site-packages\numpy\lib\tests\test_io.py:1099: with open(name, 'w') as f:
.venv\Lib\site-packages\numpy\lib\tests\test_io.py:2381: with open(name, 'w') as f:
.venv\Lib\site-packages\numpy\lib\tests\test_io.py:2398: with open(name, 'w') as f:
.venv\Lib\site-packages\numpy\lib\tests\test_loadtxt.py:967: with open(fname, "w") as fh:
.venv\Lib\site-packages\numpy\lib\tests\test_loadtxt.py:997: with open(fname, "w") as fh:
.venv\Lib\site-packages\numpy\ma\tests\test_mrecords.py:471: with open(path, 'w') as f:
.venv\Lib\site-packages\numpy\random\tests\test_extending.py:75: with open(native_file, 'w') as f:
.venv\Lib\site-packages\numpy\testing\tests\test_utils.py:2031: with open(fpath, 'w'):
.venv\Lib\site-packages\numpy\testing\tests\test_utils.py:2047: with open(fpath, 'w'):
.venv\Lib\site-packages\numpy\testing\_private\extbuild.py:124: with filename.open('w') as f:
.venv\Lib\site-packages\numpy\_core\tests\test_cython.py:60: with open(native_file, 'w') as f:
.venv\Lib\site-packages\numpy\_core\tests\test_limited_api.py:60: with open(native_file, 'w') as f:
.venv\Lib\site-packages\numpy\_core\tests\test_longdouble.py:145: with open(path, 'w') as f:
.venv\Lib\site-packages\numpy\_core\tests\test_longdouble.py:155: with open(path, 'w') as f:
.venv\Lib\site-packages\numpy\_core\tests\test_longdouble.py:163: with open(path, 'w') as f:
.venv\Lib\site-packages\numpy\_core\tests\test_longdouble.py:171: with open(path, 'w') as f:
.venv\Lib\site-packages\numpy\_core\tests\test_longdouble.py:179: with open(path, 'w') as f:
.venv\Lib\site-packages\numpy\_core\tests\test_longdouble.py:187: with open(path, 'w') as f:
.venv\Lib\site-packages\numpy\_core\tests\test_longdouble.py:195: with open(path, 'w') as f:
.venv\Lib\site-packages\numpy\_core\tests\test_longdouble.py:203: with open(path, 'w') as f:
.venv\Lib\site-packages\numpy\_core\tests\test_longdouble.py:211: with open(path, 'w') as f:
.venv\Lib\site-packages\numpy\_core\tests\test_longdouble.py:219: with open(path, 'w') as f:
.venv\Lib\site-packages\numpy\_core\tests\test_longdouble.py:229: with open(path, 'w') as f:
.venv\Lib\site-packages\numpy\_core\tests\test_longdouble.py:238: with open(path, 'w') as f:
.venv\Lib\site-packages\numpy\_core\tests\test_multiarray.py:6547: with open(tmp_filename, 'w') as f:
.venv\Lib\site-packages\numpy\_core\tests\test_multiarray.py:6555: with open(tmp_filename, 'w') as f:
.venv\Lib\site-packages\numpy\_core\tests\test_multiarray.py:6563: with open(tmp_filename, 'w') as f:
.venv\Lib\site-packages\numpy\_core\tests\test_multiarray.py:6599: with open(tmp_filename, "w") as f:
.venv\Lib\site-packages\PIL\ImagePalette.py:196: fp = open(fp, "w")
.venv\Lib\site-packages\pip\_internal\configuration.py:225: with open(fname, "w") as f:
.venv\Lib\site-packages\pip\_internal\commands\install.py:487: with open(options.json_report_file, "w", encoding="utf-8") as f:
.venv\Lib\site-packages\pip\_internal\operations\build\build_tracker.py:110: with open(entry_path, "w", encoding="utf-8") as fp:
.venv\Lib\site-packages\pip\_internal\vcs\mercurial.py:78: with open(repo_config, "w") as config_file:
.venv\Lib\site-packages\pip\_vendor\distlib\util.py:546: outstream = codecs.open(outfile, 'w', encoding=encoding)
.venv\Lib\site-packages\pip\_vendor\distlib\util.py:1679: self.stream = _csv_open(fn, 'w')
.venv\Lib\site-packages\pip\_vendor\distlib\util.py:1895: with open(fn, 'w') as f:
.venv\Lib\site-packages\pip\_vendor\pygments\unistring.py:139: with open(__file__, 'w', encoding='utf-8') as fp:
.venv\Lib\site-packages\pip\_vendor\pyproject_hooks\_impl.py:29: with open(path, "w", encoding="utf-8") as f:
.venv\Lib\site-packages\pip\_vendor\pyproject_hooks\_in_process\_in_process.py:32: with open(path, "w", encoding="utf-8") as f:
.venv\Lib\site-packages\pip\_vendor\rich\console.py:2216: with open(path, "w", encoding="utf-8") as write_file:
.venv\Lib\site-packages\pip\_vendor\rich\console.py:2322: with open(path, "w", encoding="utf-8") as write_file:
.venv\Lib\site-packages\pip\_vendor\rich\console.py:2611: with open(path, "w", encoding="utf-8") as write_file:
.venv\Lib\site-packages\pygame\_debug.py:185: with open(filename, "w", encoding="utf8") as debugfile:
.venv\Lib\site-packages\pygame\tests\test_utils\run_tests.py:309: results_file = open(option_file, "w")
.venv\Lib\site-packages\PySide6\scripts\metaobjectdump.py:505: with open(args.out_file, 'w') as f:
.venv\Lib\site-packages\PySide6\scripts\project.py:156: with self._qml_dir_file.open("w") as qf:
.venv\Lib\site-packages\PySide6\scripts\qtpy2cpp.py:60: with target_file.open("w") as file:
.venv\Lib\site-packages\PySide6\scripts\deploy_lib\config.py:54: with open(self.config_file, 'w') as config_file:
core\storage.py:31: with open(ruta_tmp, "w", encoding="utf-8") as f:
core\scrapers\store_scrapers.py:35: with open(CACHE_GIVEAWAYS_FILE, "w", encoding="utf-8") as f:
tests\test_history.py:43: with open(test_file, "w", encoding="utf-8") as f:
```

### Pattern: json\.dump\s*\(

```text
.venv\Lib\site-packages\pip\_internal\commands\install.py:488: json.dump(report.to_dict(), f, indent=2, ensure_ascii=False)
.venv\Lib\site-packages\pip\_vendor\pyproject_hooks\_impl.py:30: json.dump(obj, f, **kwargs)
.venv\Lib\site-packages\pip\_vendor\pyproject_hooks\_in_process\_in_process.py:33: json.dump(obj, f, **kwargs)
.venv\Lib\site-packages\PySide6\scripts\metaobjectdump.py:506: json.dump(json_list, f, indent=indent)
.venv\Lib\site-packages\PySide6\scripts\metaobjectdump.py:508: json.dump(json_list, sys.stdout, indent=indent)
core\storage.py:32: json.dump(datos, f, ensure_ascii=False, indent=4)
core\scrapers\store_scrapers.py:36: json.dump(giveaways, f, ensure_ascii=False, indent=2)
```


## 8. Sensitive-looking files and directories

### Potential runtime or sensitive files

```text

FullName                                                                                 
--------                                                                                 
F:\KURIGAMESDEV\KG TRACKER\.venv\Lib\site-packages\certifi\cacert.pem                    
F:\KURIGAMESDEV\KG TRACKER\.venv\Lib\site-packages\pip\_internal\cache.py                
F:\KURIGAMESDEV\KG TRACKER\.venv\Lib\site-packages\pip\_internal\commands\cache.py       
F:\KURIGAMESDEV\KG TRACKER\.venv\Lib\site-packages\pip\_internal\commands\__pycache__\...
F:\KURIGAMESDEV\KG TRACKER\.venv\Lib\site-packages\pip\_internal\network\cache.py        
F:\KURIGAMESDEV\KG TRACKER\.venv\Lib\site-packages\pip\_internal\network\__pycache__\c...
F:\KURIGAMESDEV\KG TRACKER\.venv\Lib\site-packages\pip\_internal\__pycache__\cache.cpy...
F:\KURIGAMESDEV\KG TRACKER\.venv\Lib\site-packages\pip\_vendor\cachecontrol\cache.py     
F:\KURIGAMESDEV\KG TRACKER\.venv\Lib\site-packages\pip\_vendor\cachecontrol\caches\fil...
F:\KURIGAMESDEV\KG TRACKER\.venv\Lib\site-packages\pip\_vendor\cachecontrol\caches\red...
F:\KURIGAMESDEV\KG TRACKER\.venv\Lib\site-packages\pip\_vendor\cachecontrol\caches\__p...
F:\KURIGAMESDEV\KG TRACKER\.venv\Lib\site-packages\pip\_vendor\cachecontrol\caches\__p...
F:\KURIGAMESDEV\KG TRACKER\.venv\Lib\site-packages\pip\_vendor\cachecontrol\__pycache_...
F:\KURIGAMESDEV\KG TRACKER\.venv\Lib\site-packages\pip\_vendor\certifi\cacert.pem        
F:\KURIGAMESDEV\KG TRACKER\.venv\Lib\site-packages\PySide6\qmlcachegen.exe               
F:\KURIGAMESDEV\KG TRACKER\.venv\Lib\site-packages\PySide6\Qt6LabsSettings.dll           
F:\KURIGAMESDEV\KG TRACKER\.venv\Lib\site-packages\PySide6\Qt6VirtualKeyboardSettings.dll
F:\KURIGAMESDEV\KG TRACKER\.venv\Lib\site-packages\PySide6\metatypes\qt6labssettings_m...
F:\KURIGAMESDEV\KG TRACKER\.venv\Lib\site-packages\PySide6\qml\Qt\labs\settings\qmlset...
F:\KURIGAMESDEV\KG TRACKER\.venv\Lib\site-packages\PySide6\qml\QtQuick\VirtualKeyboard...
F:\KURIGAMESDEV\KG TRACKER\.venv\Lib\site-packages\PySide6\qml\QtQuick3D\designer\Debu...
F:\KURIGAMESDEV\KG TRACKER\.venv\Lib\site-packages\PySide6\qml\QtQuick3D\designer\Debu...
F:\KURIGAMESDEV\KG TRACKER\.venv\Lib\site-packages\PySide6\qml\QtQuick3D\designer\imag...
F:\KURIGAMESDEV\KG TRACKER\.venv\Lib\site-packages\PySide6\qml\QtQuick3D\designer\imag...
F:\KURIGAMESDEV\KG TRACKER\.venv\Lib\site-packages\PySide6\qml\QtQuick3D\designer\imag...
F:\KURIGAMESDEV\KG TRACKER\.venv\Scripts\pyside6-qmlcachegen.exe                         
F:\KURIGAMESDEV\KG TRACKER\.vscode\settings.json                                         
F:\KURIGAMESDEV\KG TRACKER\assets\icons\navigation_ui\settings.png                       
F:\KURIGAMESDEV\KG TRACKER\core\ui_settings.py                                           
F:\KURIGAMESDEV\KG TRACKER\core\__pycache__\ui_settings.cpython-314.pyc                  
F:\KURIGAMESDEV\KG TRACKER\data\giveaways_cache.json                                     
F:\KURIGAMESDEV\KG TRACKER\data\giveaways_cache.json.bak                                 
F:\KURIGAMESDEV\KG TRACKER\data\reclamados.json                                          
F:\KURIGAMESDEV\KG TRACKER\data\reclamados.json.bak                                      
F:\KURIGAMESDEV\KG TRACKER\data\settings.json                                            
F:\KURIGAMESDEV\KG TRACKER\data\settings.json.bak                                        
F:\KURIGAMESDEV\KG TRACKER\data\steam_cache.json                                         
F:\KURIGAMESDEV\KG TRACKER\data\translations_cache.json                                  
F:\KURIGAMESDEV\KG TRACKER\ui\modals\settings_modal.py                                   
F:\KURIGAMESDEV\KG TRACKER\ui\modals\__pycache__\settings_modal.cpython-314.pyc          
F:\KURIGAMESDEV\KG TRACKER\ui\__pycache__\settings_modal.cpython-314.pyc
```


## 9. Network and external services

### Network pattern: https?://

```text
config.py:12: API_URL = "https://www.gamerpower.com/api/giveaways?type=game"
.venv\Lib\site-packages\charset_normalizer\api.py:357: # see https://github.com/jawah/charset_normalizer/issues/718
.venv\Lib\site-packages\charset_normalizer\api.py:358: # and https://github.com/jawah/charset_normalizer/issues/716
.venv\Lib\site-packages\charset_normalizer\api.py:515: # see https://github.com/jawah/charset_normalizer/issues/771
.venv\Lib\site-packages\charset_normalizer\legacy.py:53: # https://github.com/jawah/charset_normalizer/issues/391
.venv\Lib\site-packages\charset_normalizer\md.py:604: # see https://github.com/jawah/charset_normalizer/issues/731
.venv\Lib\site-packages\charset_normalizer\utils.py:267: # see https://github.com/jawah/charset_normalizer/issues/742
.venv\Lib\site-packages\charset_normalizer\__init__.py:17: at <https://github.com/Ousret/charset_normalizer>.
.venv\Lib\site-packages\charset_normalizer\__init__.py:46: # https://docs.python.org/3.3/howto/logging.html#configuring-logging-for-a-library
.venv\Lib\site-packages\idna\core.py:640: <https://www.unicode.org/reports/tr46/>`_: each character is kept,
.venv\Lib\site-packages\numpy\conftest.py:40: # https://hypothesis.readthedocs.io/en/latest/settings.html
.venv\Lib\site-packages\numpy\matlib.py:8: "https://docs.scipy.org/doc/numpy/user/numpy-for-matlab-users.html). "
.venv\Lib\site-packages\numpy\_array_api_info.py:6: https://data-apis.org/array-api/latest/API_specification/inspection.html for
.venv\Lib\site-packages\numpy\_array_api_info.py:44: https://data-apis.org/array-api/latest/API_specification/inspection.html
.venv\Lib\site-packages\numpy\_array_api_info.py:80: https://data-apis.org/array-api/latest/API_specification/generated/array_api.info.capabilities.html
.venv\Lib\site-packages\numpy\__init__.py:14: `the NumPy homepage <https://numpy.org>`_.
.venv\Lib\site-packages\numpy\__init__.py:17: `IPython <https://ipython.org>`_, an advanced Python shell with
.venv\Lib\site-packages\numpy\__init__.py:653: "    https://numpy.org/devdocs/release/1.20.0-notes.html#deprecations")
.venv\Lib\site-packages\numpy\__init__.py:806: See https://github.com/numpy/numpy/issues/8577 and other
.venv\Lib\site-packages\numpy\__init__.py:855: "\nhttps://numpy.org/devdocs/building/index.html"
.venv\Lib\site-packages\numpy\__init__.py:892: https://github.com/torvalds/linux/commit/7cf91a98e607c2f935dbcc177d70011e95b8faff
.venv\Lib\site-packages\numpy\ctypeslib\_ctypeslib.py:15: .. [1] "SciPy Cookbook: ctypes", https://scipy-cookbook.readthedocs.io/items/Ctypes.html
.venv\Lib\site-packages\numpy\f2py\capi_maps.py:97: # https://docs.python.org/3/c-api/arg.html#building-values
.venv\Lib\site-packages\numpy\f2py\cfuncs.py:562: #error You need to install NumPy version 0.13 or higher. See https://scipy.org/install.html
.venv\Lib\site-packages\numpy\f2py\crackfortran.py:3514: ! https://web.archive.org/web/20140822061353/http://cens.ioc.ee/projects/f2py2e
.venv\Lib\site-packages\numpy\f2py\crackfortran.py:3603: See https://github.com/numpy/numpy/pull/19388 for more information.
.venv\Lib\site-packages\numpy\f2py\f2py2e.py:192: https://numpy.org/doc/stable/f2py/index.html\n"""
.venv\Lib\site-packages\numpy\f2py\f2py2e.py:706: outmess('Using meson backend\nWill pass --lower to f2py\nSee https://numpy.org/doc/stable/f2py/buildtools/meson.html\n')
.venv\Lib\site-packages\numpy\f2py\symbolic.py:4: - J3/21-007: Draft Fortran 202x. https://j3-fortran.org/doc/year/21/21-007.pdf
.venv\Lib\site-packages\numpy\f2py\__main__.py:2: # https://web.archive.org/web/20140822061353/http://cens.ioc.ee/projects/f2py2e
.venv\Lib\site-packages\numpy\f2py\tests\test_crackfortran.py:316: https://github.com/numpy/numpy/issues/23338'''
.venv\Lib\site-packages\numpy\f2py\tests\test_quoted_character.py:1: """See https://github.com/numpy/numpy/pull/10676.
.venv\Lib\site-packages\numpy\f2py\_backends\_meson.py:155: # https://github.com/numpy/numpy/issues/24874#issuecomment-1835632293
.venv\Lib\site-packages\numpy\lib\_arraysetops_impl.py:853: # https://github.com/numpy/numpy/pull/12065.
.venv\Lib\site-packages\numpy\lib\_datasource.py:15: - URLs (http, ftp, ...) : 'http://www.scipy.org/not/real/data.txt'
.venv\Lib\site-packages\numpy\lib\_datasource.py:30: >>> fp = ds.open('http://www.google.com/') # doctest: +SKIP
.venv\Lib\site-packages\numpy\lib\_datasource.py:216: URLs require a scheme string (``http://``) to be used, without it they
.venv\Lib\site-packages\numpy\lib\_datasource.py:222: >>> repos.exists('http://www.google.com/index.html')
.venv\Lib\site-packages\numpy\lib\_datasource.py:232: >>> urlname = 'http://www.google.com/'
.venv\Lib\site-packages\numpy\lib\_datasource.py:233: >>> gfile = ds.open('http://www.google.com/')
.venv\Lib\site-packages\numpy\lib\_datasource.py:305: # BUG : URLs require a scheme string ('http://') to be used.
.venv\Lib\site-packages\numpy\lib\_datasource.py:568: >>> repos = np.lib._datasource.Repository('http://www.xyz.edu/data')
.venv\Lib\site-packages\numpy\lib\_format_impl.py:861: # https://github.com/numpy/numpy/pull/6430
.venv\Lib\site-packages\numpy\lib\_function_base_impl.py:1230: `PDF <https://www.ams.org/journals/mcom/1988-51-184/
.venv\Lib\site-packages\numpy\lib\_function_base_impl.py:2152: # See https://docs.scipy.org/doc/numpy/reference/c-api.generalized-ufuncs.html
.venv\Lib\site-packages\numpy\lib\_function_base_impl.py:3201: https://en.wikipedia.org/wiki/Window_function
.venv\Lib\site-packages\numpy\lib\_function_base_impl.py:3303: https://en.wikipedia.org/wiki/Window_function
.venv\Lib\site-packages\numpy\lib\_function_base_impl.py:3403: https://en.wikipedia.org/wiki/Window_function
.venv\Lib\site-packages\numpy\lib\_function_base_impl.py:3584: https://personal.math.ubc.ca/~cbm/aands/page_379.htm
.venv\Lib\site-packages\numpy\lib\_function_base_impl.py:3585: .. [3] https://metacpan.org/pod/distribution/Math-Cephes/lib/Math/Cephes.pod#i0:-Modified-Bessel-function-of-order-zero
.venv\Lib\site-packages\numpy\lib\_function_base_impl.py:3682: https://en.wikipedia.org/wiki/Window_function
.venv\Lib\site-packages\numpy\lib\_function_base_impl.py:3783: Resource. https://mathworld.wolfram.com/SincFunction.html
.venv\Lib\site-packages\numpy\lib\_function_base_impl.py:3785: https://en.wikipedia.org/wiki/Sinc_function
.venv\Lib\site-packages\numpy\lib\_function_base_impl.py:4974: .. [1] Wikipedia page: https://en.wikipedia.org/wiki/Trapezoidal_rule
.venv\Lib\site-packages\numpy\lib\_function_base_impl.py:4977: https://en.wikipedia.org/wiki/File:Composite_trapezoidal_rule_illustration.png
.venv\Lib\site-packages\numpy\lib\_histograms_impl.py:129: https://en.wikipedia.org/wiki/Histogram#Scott.27s_normal_reference_rule
.venv\Lib\site-packages\numpy\lib\_histograms_impl.py:132: https://digitalassets.lib.berkeley.edu/sdtr/ucb/text/34.pdf
.venv\Lib\site-packages\numpy\lib\_npyio_impl.py:1498: <https://docs.python.org/library/string.html#format-specification-mini-language>`_,
.venv\Lib\site-packages\numpy\lib\_npyio_impl.py:1883: <https://docs.scipy.org/doc/numpy/user/basics.io.genfromtxt.html>`_.
.venv\Lib\site-packages\numpy\lib\_polynomial_impl.py:590: https://en.wikipedia.org/wiki/Curve_fitting
.venv\Lib\site-packages\numpy\lib\_polynomial_impl.py:592: https://en.wikipedia.org/wiki/Polynomial_interpolation
.venv\Lib\site-packages\numpy\lib\_stride_tricks_impl.py:251: `bottleneck <https://github.com/pydata/bottleneck>`_.
.venv\Lib\site-packages\numpy\lib\_stride_tricks_impl.py:350: `moving average <https://en.wikipedia.org/wiki/Moving_average>`_:
.venv\Lib\site-packages\numpy\lib\_utils_impl.py:30: 1. Information is derived with the help of `threadpoolctl <https://pypi.org/project/threadpoolctl/>`_
.venv\Lib\site-packages\numpy\lib\__init__.py:17: # load module names. See https://github.com/networkx/networkx/issues/5838
.venv\Lib\site-packages\numpy\lib\tests\test_arraysetops.py:1252: # Regression test for https://github.com/numpy/numpy/issues/25552
.venv\Lib\site-packages\numpy\lib\tests\test_function_base.py:2823: # https://github.com/numpy/numpy/issues/4755
.venv\Lib\site-packages\numpy\lib\tests\test_function_base.py:2830: # https://github.com/numpy/numpy/issues/5297
.venv\Lib\site-packages\numpy\lib\tests\test_function_base.py:4117: # https://doi.org/10.48550/arXiv.0912.0902
.venv\Lib\site-packages\numpy\lib\tests\test_io.py:324: # http://projects.scipy.org/numpy/ticket/1517#comment:2
.venv\Lib\site-packages\numpy\lib\tests\test_recfunctions.py:840: # tests the bug in https://stackoverflow.com/q/44769632/102441
.venv\Lib\site-packages\numpy\lib\tests\test_recfunctions.py:1030: # https://github.com/numpy/numpy/issues/2346
.venv\Lib\site-packages\numpy\lib\tests\test__datasource.py:39: http_path = 'http://www.google.com/'
.venv\Lib\site-packages\numpy\lib\tests\test__datasource.py:42: http_fakepath = 'http://fake.abc.web/site/'
.venv\Lib\site-packages\numpy\linalg\_linalg.py:588: https://en.wikipedia.org/wiki/Condition_number
.venv\Lib\site-packages\numpy\linalg\_linalg.py:1044: https://en.wikipedia.org/wiki/QR_factorization
.venv\Lib\site-packages\numpy\linalg\_linalg.py:2107: https://www.mathworks.com/help/techdoc/ref/rank.html
.venv\Lib\site-packages\numpy\linalg\_linalg.py:2910: .. [2] https://en.wikipedia.org/wiki/Matrix_chain_multiplication
.venv\Lib\site-packages\numpy\linalg\__init__.py:15: - OpenBLAS: https://www.openblas.net/
.venv\Lib\site-packages\numpy\linalg\__init__.py:16: - threadpoolctl: https://github.com/joblib/threadpoolctl
.venv\Lib\site-packages\numpy\ma\tests\test_core.py:1799: # from https://github.com/numpy/numpy/pull/8590#discussion_r101126465
.venv\Lib\site-packages\numpy\ma\tests\test_core.py:5144: # the scenario raised in https://github.com/numpy/numpy/issues/27201
.venv\Lib\site-packages\numpy\ma\tests\test_core.py:5735: # https://github.com/astropy/astropy/issues/6645
.venv\Lib\site-packages\numpy\ma\tests\test_extras.py:351: # (Regression test for https://github.com/numpy/numpy/issues/2684)
.venv\Lib\site-packages\numpy\ma\tests\test_extras.py:418: # (Regression test for https://github.com/numpy/numpy/issues/10438)
.venv\Lib\site-packages\numpy\ma\tests\test_subclassing.py:93: see https://github.com/numpy/numpy/issues/4564)
.venv\Lib\site-packages\numpy\ma\tests\test_subclassing.py:164: See: https://github.com/numpy/numpy/issues/15200)
.venv\Lib\site-packages\numpy\matrixlib\defmatrix.py:122: 'https://docs.scipy.org/doc/numpy/user/'
.venv\Lib\site-packages\numpy\polynomial\chebyshev.py:108: (https://web.archive.org/web/20080221202153/https://www.math.hmc.edu/~benjamin/papers/CombTrig.pdf, pg. 4)
.venv\Lib\site-packages\numpy\polynomial\chebyshev.py:1670: https://en.wikipedia.org/wiki/Curve_fitting
.venv\Lib\site-packages\numpy\polynomial\hermite.py:1473: https://en.wikipedia.org/wiki/Curve_fitting
.venv\Lib\site-packages\numpy\polynomial\hermite_e.py:1398: https://en.wikipedia.org/wiki/Curve_fitting
.venv\Lib\site-packages\numpy\polynomial\laguerre.py:1456: https://en.wikipedia.org/wiki/Curve_fitting
.venv\Lib\site-packages\numpy\polynomial\legendre.py:1414: https://en.wikipedia.org/wiki/Curve_fitting
.venv\Lib\site-packages\numpy\random\__init__.py:204: See https://github.com/numpy/numpy/issues/4763 for a detailed discussion
.venv\Lib\site-packages\numpy\random\tests\test_generator_mt19937.py:1632: #   https://mail.python.org/pipermail/numpy-discussion/2012-September/063801.html
.venv\Lib\site-packages\numpy\random\tests\test_random.py:872: #   https://mail.python.org/pipermail/numpy-discussion/2012-September/063801.html
.venv\Lib\site-packages\numpy\random\tests\test_randomstate.py:1110: #   https://mail.python.org/pipermail/numpy-discussion/2012-September/063801.html
.venv\Lib\site-packages\numpy\random\tests\test_seed_sequence.py:14: https://gist.github.com/imneme/540829265469e673d045
.venv\Lib\site-packages\numpy\testing\_private\utils.py:143: # See http://msdn.microsoft.com/library/en-us/dnperfmo/html/perfmonpt2.asp
.venv\Lib\site-packages\numpy\testing\_private\utils.py:1965: # https://randomascii.wordpress.com/2012/02/25/comparing-floating-point-numbers-2012-edition/
.venv\Lib\site-packages\numpy\testing\_private\utils.py:2297: https://bugs.python.org/issue4180.
.venv\Lib\site-packages\numpy\tests\test_public_api.py:348: "See https://github.com/numpy/numpy/pull/19800"
.venv\Lib\site-packages\numpy\typing\mypy_plugin.py:37: .. _configuration file: https://mypy.readthedocs.io/en/stable/config_file.html
.venv\Lib\site-packages\numpy\typing\__init__.py:15: .. _typing-extensions: https://pypi.org/project/typing-extensions/
.venv\Lib\site-packages\numpy\typing\__init__.py:176: .. _generic type: https://typing.python.org/en/latest/spec/generics.html
.venv\Lib\site-packages\numpy\typing\tests\data\pass\ma.py:198: # https://github.com/numpy/numpy/issues/31737
.venv\Lib\site-packages\numpy\typing\tests\data\pass\ndarray_misc.py:191: # https://github.com/scipy/scipy/blob/a755ee77ec47a64849abe42c349936475a6c2f24/scipy/io/arff/tests/test_arffread.py#L41-L44
.venv\Lib\site-packages\numpy\typing\tests\data\pass\ndarray_misc.py:197: # regression test for https://github.com/numpy/numpy/issues/30445
.venv\Lib\site-packages\numpy\_core\einsumfunc.py:1167: implementation, can be found at https://github.com/jcmgray/einsum_bmm.
.venv\Lib\site-packages\numpy\_core\einsumfunc.py:1311: `einops <https://github.com/arogozhnikov/einops>`_ package to cover
.venv\Lib\site-packages\numpy\_core\einsumfunc.py:1314: The `opt_einsum <https://optimized-einsum.readthedocs.io/en/stable/>`_
.venv\Lib\site-packages\numpy\_core\fromnumeric.py:1014: `contiguous <https://numpy.org/doc/stable/glossary.html#term-contiguous>`_
.venv\Lib\site-packages\numpy\_core\fromnumeric.py:1036: `introsort <https://en.wikipedia.org/wiki/Introsort>`_.
.venv\Lib\site-packages\numpy\_core\fromnumeric.py:1038: `heapsort <https://en.wikipedia.org/wiki/Heapsort>`_.
.venv\Lib\site-packages\numpy\_core\fromnumeric.py:1044: `timsort <https://en.wikipedia.org/wiki/Timsort>`_
.venv\Lib\site-packages\numpy\_core\fromnumeric.py:1045: or `radix sort <https://en.wikipedia.org/wiki/Radix_sort>`_
.venv\Lib\site-packages\numpy\_core\fromnumeric.py:1056: <https://github.com/python/cpython/blob/3.7/Objects/listsort.txt>`_
.venv\Lib\site-packages\numpy\_core\fromnumeric.py:3695: https://people.eecs.berkeley.edu/~wkahan/ieee754status/IEEE754.PDF
.venv\Lib\site-packages\numpy\_core\getlimits.py:151: pp.1-70, 2008, https://doi.org/10.1109/IEEESTD.2008.4610935
.venv\Lib\site-packages\numpy\_core\getlimits.py:153: https://en.wikipedia.org/wiki/Denormal_number
.venv\Lib\site-packages\numpy\_core\multiarray.py:861: `Frobenius inner product <https://en.wikipedia.org/wiki/Frobenius_inner_product>`_
.venv\Lib\site-packages\numpy\_core\numeric.py:769: https://en.wikipedia.org/wiki/Cross-correlation
.venv\Lib\site-packages\numpy\_core\numeric.py:866: https://en.wikipedia.org/wiki/Convolution
.venv\Lib\site-packages\numpy\_core\numeric.py:2043: https://en.wikipedia.org/wiki/Two's_complement
.venv\Lib\site-packages\numpy\_core\shape_base.py:940: # https://pv.github.io/numpy-bench/#bench_shape_base.Block2D.time_block2d
.venv\Lib\site-packages\numpy\_core\_add_newdocs.py:1835: https://data-apis.org/array-api/latest/design_topics/data_interchange.html#syntax-for-data-interchange-with-dlpack
.venv\Lib\site-packages\numpy\_core\_add_newdocs.py:1838: https://dmlc.github.io/dlpack/latest/python_spec.html
.venv\Lib\site-packages\numpy\_core\_add_newdocs.py:4219: .. [1] Python 3.14 What's New, https://docs.python.org/3/whatsnew/3.14.html#whatsnew314-refcount
.venv\Lib\site-packages\numpy\_core\_exceptions.py:126: # https://en.wikipedia.org/wiki/Binary_prefix
.venv\Lib\site-packages\numpy\_core\_internal.py:293: # the CPython bug https://bugs.python.org/issue12836.
.venv\Lib\site-packages\numpy\_core\_ufunc_config.py:74: .. [1] https://en.wikipedia.org/wiki/IEEE_754
.venv\Lib\site-packages\numpy\_core\__init__.py:69: https://numpy.org/devdocs/user/troubleshooting-importerror.html
.venv\Lib\site-packages\numpy\_core\__init__.py:169: # See also: https://github.com/dask/distributed/issues/3450
.venv\Lib\site-packages\numpy\_core\tests\test_array_coercion.py:800: Ref https://github.com/numpy/numpy/issues/1468
.venv\Lib\site-packages\numpy\_core\tests\test_defchararray.py:788: """Regression test for https://github.com/numpy/numpy/issues/5982"""
.venv\Lib\site-packages\numpy\_core\tests\test_deprecations.py:29: # https://bugs.python.org/issue4180 and it is probably simplest to
.venv\Lib\site-packages\numpy\_core\tests\test_dtype.py:1549: # test for https://github.com/numpy/numpy/pull/16574#issuecomment-642660971
.venv\Lib\site-packages\numpy\_core\tests\test_function_base.py:403: # Regression test for https://github.com/numpy/numpy/pull/6659
.venv\Lib\site-packages\numpy\_core\tests\test_indexing.py:171: # https://github.com/numpy/numpy/pull/26958/files#r1854589178
.venv\Lib\site-packages\numpy\_core\tests\test_limited_api.py:200: # see https://github.com/cython/cython/issues/7914
.venv\Lib\site-packages\numpy\_core\tests\test_memmap.py:91: # see: https://bugs.python.org/issue9949
.venv\Lib\site-packages\numpy\_core\tests\test_multiarray.py:369: # Regression test for https://github.com/numpy/numpy/pull/3526
.venv\Lib\site-packages\numpy\_core\tests\test_multiarray.py:1630: # https://github.com/numpy/numpy/issues/3286
.venv\Lib\site-packages\numpy\_core\tests\test_multiarray.py:1634: # https://github.com/numpy/numpy/issues/3253
.venv\Lib\site-packages\numpy\_core\tests\test_multiarray.py:1639: # https://github.com/numpy/numpy/issues/3126
.venv\Lib\site-packages\numpy\_core\tests\test_multiarray.py:11240: # See: https://github.com/intel/x86-simd-sort/pull/39
.venv\Lib\site-packages\numpy\_core\tests\test_multiarray.py:11260: # See: https://github.com/intel/x86-simd-sort/pull/39
.venv\Lib\site-packages\numpy\_core\tests\test_multiarray.py:11455: Regression test for: https://github.com/numpy/numpy/issues/27407
.venv\Lib\site-packages\numpy\_core\tests\test_numeric.py:2253: # https://github.com/numpy/numpy/issues/27271
.venv\Lib\site-packages\numpy\_core\tests\test_records.py:477: # https://github.com/numpy/numpy/issues/2599
.venv\Lib\site-packages\numpy\_core\tests\test_records.py:482: # https://github.com/numpy/numpy/issues/3256
.venv\Lib\site-packages\numpy\_core\tests\test_records.py:489: # https://github.com/numpy/numpy/issues/3561
.venv\Lib\site-packages\numpy\_core\tests\test_records.py:495: # https://github.com/numpy/numpy/issues/4806
.venv\Lib\site-packages\numpy\_core\tests\test_regression.py:145: # https://github.com/numpy/numpy/issues/565
.venv\Lib\site-packages\numpy\_core\tests\test_scalarmath.py:622: # Values from https://en.wikipedia.org/wiki/IEEE_754
.venv\Lib\site-packages\numpy\_core\tests\test_strings.py:933: ("http://www.python.org", "://", "http", "://", "www.python.org"),
.venv\Lib\site-packages\numpy\_core\tests\test_strings.py:934: ("http://www.python.org", "?", "http://www.python.org", "", ""),
.venv\Lib\site-packages\numpy\_core\tests\test_strings.py:935: ("http://www.python.org", "http://", "", "http://", "www.python.org"),
.venv\Lib\site-packages\numpy\_core\tests\test_strings.py:936: ("http://www.python.org", "org", "http://www.python.", "org", ""),
.venv\Lib\site-packages\numpy\_core\tests\test_strings.py:937: ("http://www.python.org", ["://", "?", "http://", "org"],
.venv\Lib\site-packages\numpy\_core\tests\test_strings.py:938: ["http", "http://www.python.org", "", "http://www.python."],
.venv\Lib\site-packages\numpy\_core\tests\test_strings.py:939: ["://", "", "http://", "org"],
.venv\Lib\site-packages\numpy\_core\tests\test_strings.py:960: ("http://www.python.org", "://", "http", "://", "www.python.org"),
.venv\Lib\site-packages\numpy\_core\tests\test_strings.py:961: ("http://www.python.org", "?", "", "", "http://www.python.org"),
.venv\Lib\site-packages\numpy\_core\tests\test_strings.py:962: ("http://www.python.org", "http://", "", "http://", "www.python.org"),
.venv\Lib\site-packages\numpy\_core\tests\test_strings.py:963: ("http://www.python.org", "org", "http://www.python.", "org", ""),
.venv\Lib\site-packages\numpy\_core\tests\test_strings.py:964: ("http://www.python.org", ["://", "?", "http://", "org"],
.venv\Lib\site-packages\numpy\_core\tests\test_strings.py:965: ["http", "", "", "http://www.python."],
.venv\Lib\site-packages\numpy\_core\tests\test_strings.py:966: ["://", "", "http://", "org"],
.venv\Lib\site-packages\numpy\_core\tests\test_strings.py:967: ["www.python.org", "http://www.python.org", "www.python.org", ""]),
.venv\Lib\site-packages\numpy\_core\tests\test_ufunc.py:2535: # https://github.com/numpy/numpy/issues/4855
.venv\Lib\site-packages\numpy\_core\tests\test_umath.py:1535: # See: https://github.com/numpy/numpy/issues/19192
.venv\Lib\site-packages\numpy\_core\tests\test_umath.py:1600: # See https://github.com/numpy/numpy/issues/18005
.venv\Lib\site-packages\numpy\_core\tests\test_umath.py:1837: # See: https://github.com/numpy/numpy/issues/20448
.venv\Lib\site-packages\numpy\_core\tests\test_umath.py:1958: # see https://github.com/numpy/numpy/issues/25097
.venv\Lib\site-packages\numpy\_core\tests\test_umath.py:5034: # https://github.com/numpy/numpy/issues/6685
.venv\Lib\site-packages\numpy\_core\tests\test_umath.py:5044: # Reproduces bug https://github.com/numpy/numpy/issues/15597
.venv\Lib\site-packages\numpy\_core\tests\test_umath_accuracy.py:32: # https://stackoverflow.com/questions/1592158/convert-hex-to-float #
.venv\Lib\site-packages\numpy\_core\tests\test_umath_complex.py:602: # Testcase taken as is from https://github.com/numpy/numpy/issues/16660
.venv\Lib\site-packages\numpy\_pyinstaller\hook-numpy.py:5: https://pyinstaller.readthedocs.io/en/stable/hooks.html
.venv\Lib\site-packages\numpy\_typing\_dtype_like.py:100: # Reference: https://docs.scipy.org/doc/numpy/reference/arrays.dtypes.html
.venv\Lib\site-packages\numpy\_typing\_dtype_like.py:108: # See https://github.com/numpy/numpy/issues/16891 for more details.
.venv\Lib\site-packages\PIL\AvifImagePlugin.py:17: # to Image.open (see https://github.com/python-pillow/Pillow/issues/569)
.venv\Lib\site-packages\PIL\BlpImagePlugin.py:7: https://creativecommons.org/publicdomain/zero/1.0/
.venv\Lib\site-packages\PIL\BmpImagePlugin.py:146: # https://msdn.microsoft.com/en-us/library/windows/desktop/dd183376(v=vs.85).aspx
.venv\Lib\site-packages\PIL\BmpImagePlugin.py:148: # https://github.com/python-pillow/Pillow/issues/1293
.venv\Lib\site-packages\PIL\DdsImagePlugin.py:6: https://web.archive.org/web/20170802060935/http://oss.sgi.com/projects/ogl-sample/registry/EXT/texture_compression_s3tc.txt
.venv\Lib\site-packages\PIL\DdsImagePlugin.py:10: https://creativecommons.org/publicdomain/zero/1.0/
.venv\Lib\site-packages\PIL\EpsImagePlugin.py:148: # showpage (see https://bugs.ghostscript.com/show_bug.cgi?id=698272)
.venv\Lib\site-packages\PIL\EpsImagePlugin.py:314: # https://www.adobe.com/devnet-apps/photoshop/fileformatashtml/#50577413_pgfId-1035096
.venv\Lib\site-packages\PIL\EpsImagePlugin.py:395: # https://web.archive.org/web/20160528181353/http://partners.adobe.com/public/developer/en/ps/5002.EPSF_Spec.pdf
.venv\Lib\site-packages\PIL\FtexImagePlugin.py:7: https://creativecommons.org/publicdomain/zero/1.0/
.venv\Lib\site-packages\PIL\GbrImagePlugin.py:17: # See https://github.com/GNOME/gimp/blob/mainline/devel-docs/gbr.txt for
.venv\Lib\site-packages\PIL\GifImagePlugin.py:1058: # https://www.matthewflickinger.com/lab/whatsinagif/bits_and_bytes.asp
.venv\Lib\site-packages\PIL\IcoImagePlugin.py:18: # https://code.google.com/archive/p/casadebender/wikis/Win32IconImagePlugin.wiki
.venv\Lib\site-packages\PIL\IcoImagePlugin.py:26: #     https://www.apache.org/licenses/LICENSE-2.0
.venv\Lib\site-packages\PIL\IcoImagePlugin.py:35: #   * https://en.wikipedia.org/wiki/ICO_(file_format)
.venv\Lib\site-packages\PIL\IcoImagePlugin.py:36: #   * https://msdn.microsoft.com/en-us/library/ms997538.aspx
.venv\Lib\site-packages\PIL\IcoImagePlugin.py:336: https://code.google.com/archive/p/casadebender/wikis/Win32IconImagePlugin.wiki
.venv\Lib\site-packages\PIL\Image.py:810: # See: https://github.com/python-pillow/Pillow/issues/350
.venv\Lib\site-packages\PIL\ImageCms.py:51: https://www.cazabon.com
.venv\Lib\site-packages\PIL\ImageCms.py:53: pyCMS home page:  https://www.cazabon.com/pyCMS
.venv\Lib\site-packages\PIL\ImageCms.py:54: littleCMS home page:  https://www.littlecms.com
.venv\Lib\site-packages\PIL\ImageColor.py:169: # X11 colour table from https://drafts.csswg.org/css-color-4/, with
.venv\Lib\site-packages\PIL\ImageEnhance.py:9: # at http://www.graficaobscura.com/interp/index.html
.venv\Lib\site-packages\PIL\ImageFilter.py:189: <https://www.mia.uni-saarland.de/Publications/gwosdek-ssvm11.pdf>
.venv\Lib\site-packages\PIL\ImageFilter.py:252: .. _digital unsharp masking: https://en.wikipedia.org/wiki/Unsharp_masking#Digital_unsharp_masking
.venv\Lib\site-packages\PIL\ImageFont.py:389: https://learn.microsoft.com/en-us/typography/opentype/spec/featurelist
.venv\Lib\site-packages\PIL\ImageFont.py:397: <https://www.w3.org/International/articles/language-tags/>`_
.venv\Lib\site-packages\PIL\ImageFont.py:443: https://learn.microsoft.com/en-us/typography/opentype/spec/featurelist
.venv\Lib\site-packages\PIL\ImageFont.py:451: <https://www.w3.org/International/articles/language-tags/>`_
.venv\Lib\site-packages\PIL\ImageFont.py:512: https://learn.microsoft.com/en-us/typography/opentype/spec/featurelist
.venv\Lib\site-packages\PIL\ImageFont.py:522: <https://www.w3.org/International/articles/language-tags/>`_
.venv\Lib\site-packages\PIL\ImageFont.py:605: https://learn.microsoft.com/en-us/typography/opentype/spec/featurelist
.venv\Lib\site-packages\PIL\ImageFont.py:615: <https://www.w3.org/International/articles/language-tags/>`_
.venv\Lib\site-packages\PIL\ImageFont.py:722: # https://savannah.nongnu.org/bugs/?56186
.venv\Lib\site-packages\PIL\ImageFont.py:1091: https://dotcolon.net/fonts/aileron, with a more limited character set.
.venv\Lib\site-packages\PIL\ImageOps.py:556: # https://www.cazabon.com
.venv\Lib\site-packages\PIL\ImageQt.py:198: # Fixes https://github.com/python-pillow/Pillow/issues/1370
.venv\Lib\site-packages\PIL\Jpeg2KImagePlugin.py:351: # https://github.com/python-pillow/Pillow/issues/4343 found that the
.venv\Lib\site-packages\PIL\JpegImagePlugin.py:108: elif marker == 0xFFE1 and s.startswith(b"http://ns.adobe.com/xap/1.0/\x00"):
.venv\Lib\site-packages\PIL\JpegImagePlugin.py:335: # Magic number was taken from https://en.wikipedia.org/wiki/JPEG
.venv\Lib\site-packages\PIL\JpegImagePlugin.py:763: overhead_len = 29  # b"http://ns.adobe.com/xap/1.0/\x00"
.venv\Lib\site-packages\PIL\JpegImagePlugin.py:769: extra += b"\xff\xe1" + size + b"http://ns.adobe.com/xap/1.0/\x00" + xmp
.venv\Lib\site-packages\PIL\JpegImagePlugin.py:828: # https://github.com/matthewwithanm/django-imagekit/issues/50
.venv\Lib\site-packages\PIL\JpegPresets.py:31: (ref.: https://en.wikipedia.org/wiki/Chroma_subsampling)
.venv\Lib\site-packages\PIL\JpegPresets.py:40: (ref.: https://exiv2.org/tags.html)
.venv\Lib\site-packages\PIL\JpegPresets.py:48: (ref.: https://en.wikipedia.org/wiki/Quantization_matrix#Quantization_matrices,
.venv\Lib\site-packages\PIL\JpegPresets.py:49: https://en.wikipedia.org/wiki/JPEG#Quantization)
.venv\Lib\site-packages\PIL\JpegPresets.py:62: https://web.archive.org/web/20120328125543/http://www.jpegcameras.com/libjpeg/libjpeg-3.html
.venv\Lib\site-packages\PIL\MspImagePlugin.py:19: # More info on this format: https://archive.org/details/gg243631
.venv\Lib\site-packages\PIL\MspImagePlugin.py:24: # See also: https://www.fileformat.info/format/mspaint/egff.htm
.venv\Lib\site-packages\PIL\MspImagePlugin.py:80: # https://www.fileformat.info/format/mspaint/egff.htm
.venv\Lib\site-packages\PIL\PdfParser.py:373: https://www.adobe.com/content/dam/acom/en/devnet/acrobat/pdfs/PDF32000_2008.pdf
.venv\Lib\site-packages\PIL\SpiderImagePlugin.py:30: # https://spider.wadsworth.org/spider_doc/spider/docs/spider.html
.venv\Lib\site-packages\PIL\SpiderImagePlugin.py:33: # https://spider.wadsworth.org/spider_doc/spider/docs/image_doc.html
.venv\Lib\site-packages\PIL\SunImagePlugin.py:124: # (https://www.fileformat.info/format/sunraster/egff.htm)
.venv\Lib\site-packages\PIL\TiffImagePlugin.py:124: # https://github.com/imagej/ImageJA/blob/master/src/main/java/ij/io/TiffDecoder.java
.venv\Lib\site-packages\PIL\TiffImagePlugin.py:822: # remerge of https://github.com/python-pillow/Pillow/pull/1416
.venv\Lib\site-packages\PIL\TiffImagePlugin.py:1284: https://www.adobe.com/devnet-apps/photoshop/fileformatashtml/#50577409_pgfId-1037727
.venv\Lib\site-packages\PIL\TiffImagePlugin.py:1582: # https://github.com/python-pillow/Pillow/issues/279
.venv\Lib\site-packages\PIL\WalImageFile.py:17: https://www.flipcode.com/archives/Quake_2_BSP_File_Format.shtml
.venv\Lib\site-packages\PIL\WmfImagePlugin.py:18: # https://winprotocoldoc.blob.core.windows.net/productionwindowsarchives/MS-WMF/[MS-WMF].pdf
.venv\Lib\site-packages\PIL\WmfImagePlugin.py:19: # http://wvware.sourceforge.net/caolan/index.html
.venv\Lib\site-packages\PIL\WmfImagePlugin.py:20: # http://wvware.sourceforge.net/caolan/ora-wmf.html
.venv\Lib\site-packages\PIL\__init__.py:4: https://github.com/python-pillow/Pillow/
.venv\Lib\site-packages\pip\__init__.py:9: For additional details, see https://github.com/pypa/pip/issues/7498.
.venv\Lib\site-packages\pip\_internal\cache.py:60: # https://github.com/pypa/pip/issues/7296
.venv\Lib\site-packages\pip\_internal\cache.py:284: # https://github.com/pypa/pip/pull/10564 is merged.
.venv\Lib\site-packages\pip\_internal\configuration.py:299: # See https://github.com/pypa/pip/issues/4963
.venv\Lib\site-packages\pip\_internal\configuration.py:305: # See https://github.com/pypa/pip/issues/4893
.venv\Lib\site-packages\pip\_internal\exceptions.py:1017: link="https://pip.pypa.io/en/stable/topics/dependency-resolution/#handling-resolution-too-deep-errors",
.venv\Lib\site-packages\pip\_internal\exceptions.py:1076: "tracker: https://github.com/pypa/pip/issues/new"
.venv\Lib\site-packages\pip\_internal\main.py:8: For additional details, see https://github.com/pypa/pip/issues/7498.
.venv\Lib\site-packages\pip\_internal\__init__.py:14: For additional details, see https://github.com/pypa/pip/issues/7498.
.venv\Lib\site-packages\pip\_internal\cli\cmdoptions.py:95: "    https://pip.pypa.io/en/stable/user_guide/#installing-only-dependencies"
.venv\Lib\site-packages\pip\_internal\cli\cmdoptions.py:498: https://packaging.python.org/en/latest/specifications/simple-repository-api/
.venv\Lib\site-packages\pip\_internal\cli\index_command.py:83: # then https://github.com/python/mypy/issues/7696 kicks in
.venv\Lib\site-packages\pip\_internal\cli\main.py:21: # https://pip.pypa.io/en/stable/user_guide/#using-pip-from-your-program.
.venv\Lib\site-packages\pip\_internal\cli\spinners.py:227: # See https://github.com/pypa/pip/issues/3418
.venv\Lib\site-packages\pip\_internal\commands\cache.py:253: # PEP 427: https://www.python.org/dev/peps/pep-0427/
.venv\Lib\site-packages\pip\_internal\commands\configuration.py:40: "pip config set global.index-url https://example.org/" would configure
.venv\Lib\site-packages\pip\_internal\commands\install.py:666: "pip's issue tracker: https://github.com/pypa/pip/issues/new"
.venv\Lib\site-packages\pip\_internal\commands\install.py:902: "https://pip.pypa.io/warnings/enable-long-paths\n"
.venv\Lib\site-packages\pip\_internal\commands\wheel.py:28: wheel docs: https://wheel.readthedocs.io/en/latest/
.venv\Lib\site-packages\pip\_internal\commands\wheel.py:31: https://pip.pypa.io/en/stable/reference/build-system/
.venv\Lib\site-packages\pip\_internal\locations\_distutils.py:10: # See https://github.com/pypa/pip/issues/8761 for the original discussion and
.venv\Lib\site-packages\pip\_internal\locations\_distutils.py:127: https://docs.python.org/3/install/index.html#alternate-installation
.venv\Lib\site-packages\pip\_internal\locations\__init__.py:51: Rationale in https://github.com/pypa/pip/issues/10647
.venv\Lib\site-packages\pip\_internal\locations\__init__.py:78: See <https://bugs.python.org/issue44860>.
.venv\Lib\site-packages\pip\_internal\locations\__init__.py:178: issue_url = "https://github.com/pypa/pip/issues/10151"
.venv\Lib\site-packages\pip\_internal\locations\__init__.py:332: # https://github.com/python/cpython/blob/8c21941ddaf/Lib/sysconfig.py#L178-L194
.venv\Lib\site-packages\pip\_internal\locations\__init__.py:364: "at https://github.com/Homebrew/homebrew-core/issues/76621"
.venv\Lib\site-packages\pip\_internal\metadata\base.py:178: #       (https://github.com/pypa/pip/issues/10243)
.venv\Lib\site-packages\pip\_internal\metadata\_json.py:1: # Extracted from https://github.com/pfmoore/pkg_metadata
.venv\Lib\site-packages\pip\_internal\models\index.py:25: PyPI = PackageIndex("https://pypi.org/", file_storage_domain="files.pythonhosted.org")
.venv\Lib\site-packages\pip\_internal\models\index.py:27: "https://test.pypi.org/", file_storage_domain="test-files.pythonhosted.org"
.venv\Lib\site-packages\pip\_internal\models\installation_report.py:32: # requirement. https://peps.python.org/pep-0376/#requested
.venv\Lib\site-packages\pip\_internal\models\installation_report.py:35: # https://www.python.org/dev/peps/pep-0566/#json-compatible-metadata
.venv\Lib\site-packages\pip\_internal\models\installation_report.py:50: # https://peps.python.org/pep-0508/#environment-markers
.venv\Lib\site-packages\pip\_internal\models\installation_report.py:55: # https://github.com/pypa/pip/issues/11198
.venv\Lib\site-packages\pip\_internal\models\link.py:235: if url.startswith(("https://", "http://")):
.venv\Lib\site-packages\pip\_internal\models\scheme.py:5: https://docs.python.org/3/install/index.html#alternate-installation.
.venv\Lib\site-packages\pip\_internal\network\cache.py:46: files (https://github.com/psf/cachecontrol/issues/324).  We therefore have
.venv\Lib\site-packages\pip\_internal\network\download.py:367: # https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Range_requests
.venv\Lib\site-packages\pip\_internal\network\session.py:72: # Taken from Chrome's list of secure origins (See: http://bit.ly/1qrySKC)
.venv\Lib\site-packages\pip\_internal\network\session.py:265: # context here too. https://github.com/pypa/pip/issues/13288
.venv\Lib\site-packages\pip\_internal\network\session.py:271: # https://github.com/pypa/pip/issues/13465
.venv\Lib\site-packages\pip\_internal\network\session.py:367: # support caching so we'll use it for all http:// URLs.
.venv\Lib\site-packages\pip\_internal\network\session.py:369: # https:// hosts that we've marked as ignoring
.venv\Lib\site-packages\pip\_internal\network\session.py:393: self.mount("https://", secure_adapter)
.venv\Lib\site-packages\pip\_internal\network\session.py:394: self.mount("http://", insecure_adapter)
.venv\Lib\site-packages\pip\_internal\operations\prepare.py:238: TODO: once https://github.com/pypa/packaging/pull/1278 is released and
.venv\Lib\site-packages\pip\_internal\operations\prepare.py:763: # FIXME: https://github.com/pypa/pip/issues/11943
.venv\Lib\site-packages\pip\_internal\operations\install\wheel.py:210: # https://github.com/pypa/pip/issues/5868
.venv\Lib\site-packages\pip\_internal\operations\install\wheel.py:391: "suffix is required. See https://packaging.python.org/"
.venv\Lib\site-packages\pip\_internal\operations\install\wheel.py:652: # See https://github.com/pypa/pip/issues/1800
.venv\Lib\site-packages\pip\_internal\operations\install\wheel.py:657: # See https://bitbucket.org/pypa/distlib/issue/35/
.venv\Lib\site-packages\pip\_internal\operations\install\wheel.py:662: # See https://bitbucket.org/pypa/distlib/issue/32/
.venv\Lib\site-packages\pip\_internal\req\constructors.py:53: # https://packaging.python.org/en/latest/specifications/version-specifiers/#id5
.venv\Lib\site-packages\pip\_internal\req\constructors.py:82: # see https://peps.python.org/pep-0508/#complete-grammar
.venv\Lib\site-packages\pip\_internal\req\constructors.py:146: - svn+http://blahblah@rev#egg=Foobar[baz]&subdirectory=version_subdir
.venv\Lib\site-packages\pip\_internal\req\constructors.py:148: - Foobar[extra] @ svn+http://blahblah@rev#subdirectory=subdir ; markers
.venv\Lib\site-packages\pip\_internal\req\req_file.py:490: #       https://github.com/python/mypy/issues/2427
.venv\Lib\site-packages\pip\_internal\req\req_file.py:546: request #3514 <https://github.com/pypa/pip/pull/3514>`_.
.venv\Lib\site-packages\pip\_internal\req\req_file.py:549: <http://pubs.opengroup.org/onlinepubs/9699919799/>`_ and are limited
.venv\Lib\site-packages\pip\_internal\req\req_uninstall.py:70: https://packaging.python.org/specifications/recording-installed-packages/
.venv\Lib\site-packages\pip\_internal\resolution\resolvelib\factory.py:712: # https://github.com/pypa/pip/issues/11745#issuecomment-1402805842
.venv\Lib\site-packages\pip\_internal\resolution\resolvelib\factory.py:899: "https://pip.pypa.io/en/latest/topics/dependency-resolution/"
.venv\Lib\site-packages\pip\_internal\resolution\resolvelib\resolver.py:289: # See https://github.com/pypa/pip/issues/10557
.venv\Lib\site-packages\pip\_internal\utils\appdirs.py:41: # see <https://github.com/pypa/pip/issues/1733>
.venv\Lib\site-packages\pip\_internal\utils\compat.py:48: https://github.com/pypa/pip/pull/935#discussion_r5307003
.venv\Lib\site-packages\pip\_internal\utils\compatibility_tags.py:86: # https://www.python.org/dev/peps/pep-0599/#backwards-compatibility-with-manylinux2010-wheels
.venv\Lib\site-packages\pip\_internal\utils\compatibility_tags.py:94: # https://www.python.org/dev/peps/pep-0571/#backwards-compatibility-with-manylinux1-wheels
.venv\Lib\site-packages\pip\_internal\utils\deprecation.py:128: "Discussion can be found at https://github.com/pypa/pip/issues/{}",
.venv\Lib\site-packages\pip\_internal\utils\egg_link.py:26: the way it names .egg-link files (https://github.com/pypa/setuptools/issues/4167).
.venv\Lib\site-packages\pip\_internal\utils\entrypoints.py:39: "Please see https://github.com/pypa/pip/issues/5599 for advice on "
.venv\Lib\site-packages\pip\_internal\utils\filesystem.py:95: # os.access doesn't work on Windows: http://bugs.python.org/issue2528
.venv\Lib\site-packages\pip\_internal\utils\filesystem.py:96: # and we can't use tempfile: http://bugs.python.org/issue22107
.venv\Lib\site-packages\pip\_internal\utils\glibc.py:17: # https://github.com/python/cpython/blob/fcf1d003bf4f0100c9d0921ff3d70e1127ca1b71/Lib/platform.py#L175-L183
.venv\Lib\site-packages\pip\_internal\utils\logging.py:51: # https://bugs.python.org/issue19612
.venv\Lib\site-packages\pip\_internal\utils\logging.py:52: # https://bugs.python.org/issue30418
.venv\Lib\site-packages\pip\_internal\utils\misc.py:75: # For more background, see: https://github.com/pypa/pip/issues/5499
.venv\Lib\site-packages\pip\_internal\utils\misc.py:161: # See https://docs.python.org/3.12/whatsnew/3.12.html#shutil.
.venv\Lib\site-packages\pip\_internal\utils\misc.py:615: # See https://github.com/pypa/pip/issues/1299 for more discussion
.venv\Lib\site-packages\pip\_internal\utils\misc.py:790: # checks: https://mypy.readthedocs.io/en/stable/common_issues.html
.venv\Lib\site-packages\pip\_internal\utils\misc.py:802: "https://pip.pypa.io/warnings/venv. "
.venv\Lib\site-packages\pip\_internal\utils\unpacking.py:228: # (https://github.com/python/cpython/issues/107845)
.venv\Lib\site-packages\pip\_internal\utils\_jaraco_text.py:73: >>> drop_comment('http://example.com/foo#bar')
.venv\Lib\site-packages\pip\_internal\utils\_jaraco_text.py:74: 'http://example.com/foo#bar'
.venv\Lib\site-packages\pip\_internal\vcs\git.py:73: # https://github.com/pypa/pip/issues/1130
.venv\Lib\site-packages\pip\_internal\vcs\git.py:287: # https://git-scm.com/docs/partial-clone
.venv\Lib\site-packages\pip\_internal\vcs\git.py:507: # (see https://article.gmane.org/gmane.comp.version-control.git/146500)
.venv\Lib\site-packages\pip\_internal\vcs\versioncontrol.py:386: "e.g. svn+http://myrepo/svn/MyApp#egg=MyApp"
.venv\Lib\site-packages\pip\_internal\vcs\versioncontrol.py:548: # https://github.com/python/mypy/issues/1174
.venv\Lib\site-packages\pip\_internal\vcs\versioncontrol.py:668: f"https://pip.pypa.io/en/latest/reference/pip_freeze/"
.venv\Lib\site-packages\pip\_vendor\__init__.py:28: # https://github.com/kennethreitz/requests/pull/2567.
.venv\Lib\site-packages\pip\_vendor\cachecontrol\controller.py:91: # https://tools.ietf.org/html/rfc7234#section-5.2
.venv\Lib\site-packages\pip\_vendor\cachecontrol\controller.py:198: #   https://tools.ietf.org/html/rfc7231#section-6.4.2
.venv\Lib\site-packages\pip\_vendor\cachecontrol\controller.py:399: # https://tools.ietf.org/html/rfc7234#section-4.1:
.venv\Lib\site-packages\pip\_vendor\cachecontrol\controller.py:489: # http://tools.ietf.org/html/draft-ietf-httpbis-p4-conditional-26#section-4.1
.venv\Lib\site-packages\pip\_vendor\cachecontrol\filewrapper.py:49: # [0] https://docs.python.org/2/reference/expressions.html#atom-identifiers
.venv\Lib\site-packages\pip\_vendor\cachecontrol\heuristics.py:34: http://tools.ietf.org/html/rfc7234#section-5.5.4 where we need
.venv\Lib\site-packages\pip\_vendor\cachecontrol\heuristics.py:101: http://tools.ietf.org/html/rfc7234#section-4.2.2
.venv\Lib\site-packages\pip\_vendor\cachecontrol\heuristics.py:105: https://developer.mozilla.org/en-US/docs/Web/HTTP/Caching_FAQ
.venv\Lib\site-packages\pip\_vendor\cachecontrol\heuristics.py:106: http://lxr.mozilla.org/mozilla-release/source/netwerk/protocol/http/nsHttpResponseHead.cpp#397
.venv\Lib\site-packages\pip\_vendor\cachecontrol\wrapper.py:40: sess.mount("http://", adapter)
.venv\Lib\site-packages\pip\_vendor\cachecontrol\wrapper.py:41: sess.mount("https://", adapter)
.venv\Lib\site-packages\pip\_vendor\cachecontrol\_cmd.py:33: sess.mount("http://", adapter)
.venv\Lib\site-packages\pip\_vendor\cachecontrol\_cmd.py:34: sess.mount("https://", adapter)
.venv\Lib\site-packages\pip\_vendor\cachecontrol\caches\file_cache.py:60: #       See: https://github.com/ionrock/cachecontrol/issues/63
.venv\Lib\site-packages\pip\_vendor\distlib\compat.py:95: http://tools.ietf.org/html/rfc6125#section-6.4.3
.venv\Lib\site-packages\pip\_vendor\distlib\compat.py:628: # {{{ http://code.activestate.com/recipes/576693/ (r9)
.venv\Lib\site-packages\pip\_vendor\distlib\scripts.py:54: # This is to address https://github.com/pypa/pip/issues/12666.
.venv\Lib\site-packages\pip\_vendor\distlib\scripts.py:157: See also: http://www.in-ulm.de/~mascheck/various/shebang/#length
.venv\Lib\site-packages\pip\_vendor\distlib\scripts.py:158: https://hg.mozilla.org/mozilla-central/file/tip/mach
.venv\Lib\site-packages\pip\_vendor\distlib\scripts.py:406: # Launchers are from https://bitbucket.org/vinay.sajip/simple_launcher/
.venv\Lib\site-packages\pip\_vendor\distlib\util.py:951: _external_data_base_url = 'https://www.red-dove.com/pypi/projects/'
.venv\Lib\site-packages\pip\_vendor\distlib\util.py:1158: # http://en.wikipedia.org/wiki/Tarjan%27s_strongly_connected_components_algorithm
.venv\Lib\site-packages\pip\_vendor\distlib\util.py:1296: # See: https://docs.python.org/3/library/tarfile.html#extraction-filters
.venv\Lib\site-packages\pip\_vendor\distlib\util.py:1550: # HTML containing a http://xyz link when it should be https://xyz),
.venv\Lib\site-packages\pip\_vendor\distlib\util.py:1802: # https://peps.python.org/pep-0503/#normalized-names
.venv\Lib\site-packages\pip\_vendor\distlib\util.py:1824: DEFAULT_REPOSITORY = 'https://upload.pypi.org/legacy/'
.venv\Lib\site-packages\pip\_vendor\distro\distro.py:8: # http://www.apache.org/licenses/LICENSE-2.0
.venv\Lib\site-packages\pip\_vendor\distro\distro.py:28: <https://bugs.python.org/issue1322>`_ for more information.
.venv\Lib\site-packages\pip\_vendor\distro\distro.py:442: <http://www.freedesktop.org/software/systemd/man/os-release.html>`_.
.venv\Lib\site-packages\pip\_vendor\distro\distro.py:1330: # See https://github.com/python-distro/distro/issues/162
.venv\Lib\site-packages\pip\_vendor\idna\core.py:458: <https://www.unicode.org/reports/tr46/>`_: each character is kept,
.venv\Lib\site-packages\pip\_vendor\packaging\markers.py:237: # https://peps.python.org/pep-0685/
.venv\Lib\site-packages\pip\_vendor\packaging\tags.py:737: <https://developer.android.com/tools/releases/platforms>`__ to return. Defaults
.venv\Lib\site-packages\pip\_vendor\packaging\tags.py:739: :param str abi: The `Android ABI <https://developer.android.com/ndk/guides/abis>`__,
.venv\Lib\site-packages\pip\_vendor\packaging\utils.py:269: .. _Source distribution format: https://packaging.python.org/specifications/source-distribution-format/#source-distribution-file-name
.venv\Lib\site-packages\pip\_vendor\packaging\version.py:232: # CPython 3.11.0-3.11.4 had a bug: https://github.com/python/cpython/pull/107795
.venv\Lib\site-packages\pip\_vendor\packaging\_elffile.py:7: ELF header: https://refspecs.linuxfoundation.org/elf/gabi4+/ch4.eheader.html
.venv\Lib\site-packages\pip\_vendor\packaging\_manylinux.py:43: # https://static.docs.arm.com/ihi0044/g/aaelf32.pdf
.venv\Lib\site-packages\pip\_vendor\packaging\_manylinux.py:93: # https://github.com/python/cpython/blob/fcf1d003bf4f0100c/Lib/platform.py#L175-L183
.venv\Lib\site-packages\pip\_vendor\packaging\_manylinux.py:240: # https://sourceware.org/bugzilla/show_bug.cgi?id=24636
.venv\Lib\site-packages\pip\_vendor\packaging\__init__.py:7: __uri__ = "https://github.com/pypa/packaging"
.venv\Lib\site-packages\pip\_vendor\packaging\licenses\__init__.py:4: #  https://github.com/pypa/hatch/blob/5352e44/backend/src/hatchling/licenses/parse.py
.venv\Lib\site-packages\pip\_vendor\pkg_resources\__init__.py:109: # See https://github.com/pypa/pip/issues/12243
.venv\Lib\site-packages\pip\_vendor\pkg_resources\__init__.py:134: # Use _typeshed.importlib.LoaderProtocol once available https://github.com/python/typeshed/pull/11890
.venv\Lib\site-packages\pip\_vendor\pkg_resources\__init__.py:1756: https://setuptools.pypa.io/en/latest/pkg_resources.html#basic-resource-access
.venv\Lib\site-packages\pip\_vendor\pkg_resources\__init__.py:2514: "See https://setuptools.pypa.io/en/latest/references/"
.venv\Lib\site-packages\pip\_vendor\pkg_resources\__init__.py:2620: # https://github.com/python/mypy/issues/16261
.venv\Lib\site-packages\pip\_vendor\pkg_resources\__init__.py:2621: # https://github.com/python/typeshed/issues/6347
.venv\Lib\site-packages\pip\_vendor\platformdirs\android.py:17: Follows the guidance `from here <https://android.stackexchange.com/a/216132>`_. Directories are typically located
.venv\Lib\site-packages\pip\_vendor\platformdirs\android.py:175: # https://stackoverflow.com/a/61394121
.venv\Lib\site-packages\pip\_vendor\platformdirs\api.py:72: login (see `here <https://technet.microsoft.com/en-us/library/cc766489(WS.10).aspx>`_).
.venv\Lib\site-packages\pip\_vendor\platformdirs\macos.py:23: <https://developer.apple.com/library/archive/documentation/FileManagement/Conceptual/FileSystemProgrammingGuide/MacOSXDirectories/MacOSXDirectories.html>`_.
.venv\Lib\site-packages\pip\_vendor\platformdirs\macos.py:73: """:returns: cache directory shared by users, e.g. ``/Library/Caches/$appname/$version``. If we're using a Python binary managed by `Homebrew <https://brew.sh>`_, the directory will be under the Homebrew prefix, e.g. ``$homebrew_prefix/var/cache/$appname/$version``. If `multipath <platformdirs.api.PlatformDirsABC.multipath>` is enabled, and we're in Homebrew, the response is a multi-path string separated by ":", e.g. ``$homebrew_prefix/var/cache/$appname/$version:/Library/Caches/$appname/$version``"""
.venv\Lib\site-packages\pip\_vendor\platformdirs\macos.py:212: <https://developer.apple.com/library/archive/documentation/FileManagement/Conceptual/FileSystemProgrammingGuide/MacOSXDirectories/MacOSXDirectories.html>`_.
.venv\Lib\site-packages\pip\_vendor\platformdirs\unix.py:239: """On Unix/Linux, we follow the `XDG Basedir Spec <https://specifications.freedesktop.org/basedir/latest/>`_.
.venv\Lib\site-packages\pip\_vendor\platformdirs\unix.py:299: See https://freedesktop.org/wiki/Software/xdg-user-dirs/.
.venv\Lib\site-packages\pip\_vendor\platformdirs\windows.py:20: """`MSDN on where to store app data files <https://learn.microsoft.com/en-us/windows/win32/shell/knownfolderid>`_.
.venv\Lib\site-packages\pip\_vendor\platformdirs\windows.py:308: See https://learn.microsoft.com/en-us/windows/win32/api/shlobj_core/nf-shlobj_core-shgetknownfolderpath.
.venv\Lib\site-packages\pip\_vendor\platformdirs\__init__.py:6: See <https://github.com/platformdirs/platformdirs> for details and usage.
.venv\Lib\site-packages\pip\_vendor\platformdirs\__init__.py:48: # Work around mypy issue: https://github.com/python/mypy/issues/10962
.venv\Lib\site-packages\pip\_vendor\pygments\lexer.py:220: 'from http://chardet.feedparser.org/') from e
.venv\Lib\site-packages\pip\_vendor\pygments\util.py:226: # http://www.unicode.org/book/ch03.pdf
.venv\Lib\site-packages\pip\_vendor\pygments\__init__.py:22: https://github.com/pygments/pygments/archive/master.zip#egg=Pygments-dev
.venv\Lib\site-packages\pip\_vendor\pygments\lexers\python.py:35: url = 'https://www.python.org'
.venv\Lib\site-packages\pip\_vendor\pygments\lexers\python.py:187: (r'(=\s*)?'         # debug (https://bugs.python.org/issue36817)
.venv\Lib\site-packages\pip\_vendor\pygments\lexers\python.py:192: (r'(=\s*)?'         # debug (https://bugs.python.org/issue36817)
.venv\Lib\site-packages\pip\_vendor\pygments\lexers\python.py:205: # Based on https://docs.python.org/3/reference/expressions.html
.venv\Lib\site-packages\pip\_vendor\pygments\lexers\python.py:429: url = 'https://www.python.org'
.venv\Lib\site-packages\pip\_vendor\pygments\lexers\python.py:705: url = 'https://python.org'
.venv\Lib\site-packages\pip\_vendor\pygments\lexers\python.py:740: url = 'https://python.org'
.venv\Lib\site-packages\pip\_vendor\pygments\lexers\python.py:770: # Either `PEP 657 <https://www.python.org/dev/peps/pep-0657/>`
.venv\Lib\site-packages\pip\_vendor\pygments\lexers\python.py:797: url = 'https://python.org'
.venv\Lib\site-packages\pip\_vendor\pygments\lexers\python.py:838: url = 'https://cython.org'
.venv\Lib\site-packages\pip\_vendor\pygments\lexers\python.py:1022: url = 'http://pyos.github.io/dg'
.venv\Lib\site-packages\pip\_vendor\pygments\lexers\python.py:1117: url = 'https://numpy.org/'
.venv\Lib\site-packages\pip\_vendor\requests\adapters.py:182: >>> s.mount('http://', a)
.venv\Lib\site-packages\pip\_vendor\requests\adapters.py:531: "https://github.com/psf/requests/pull/6710 for more details."
.venv\Lib\site-packages\pip\_vendor\requests\api.py:62: >>> req = requests.request('GET', 'https://httpbin.org/get')
.venv\Lib\site-packages\pip\_vendor\requests\auth.py:281: # See https://github.com/psf/requests/issues/3772
.venv\Lib\site-packages\pip\_vendor\requests\compat.py:88: proxy_bypass_environment,  # type: ignore[attr-defined]  # https://github.com/python/cpython/issues/145331
.venv\Lib\site-packages\pip\_vendor\requests\models.py:14: # such as in Embedded Python. See https://github.com/psf/requests/issues/3578.
.venv\Lib\site-packages\pip\_vendor\requests\models.py:306: >>> req = requests.Request('GET', 'https://httpbin.org/get')
.venv\Lib\site-packages\pip\_vendor\requests\models.py:387: >>> req = requests.Request('GET', 'https://httpbin.org/get')
.venv\Lib\site-packages\pip\_vendor\requests\models.py:491: #: https://github.com/psf/requests/pull/2238
.venv\Lib\site-packages\pip\_vendor\requests\models.py:516: f"Perhaps you meant https://{url}?"
.venv\Lib\site-packages\pip\_vendor\requests\sessions.py:238: # (e.g. '/path/to/resource' instead of 'http://domain.tld/path/to/resource')
.venv\Lib\site-packages\pip\_vendor\requests\sessions.py:249: # https://github.com/psf/requests/issues/1084
.venv\Lib\site-packages\pip\_vendor\requests\sessions.py:254: # https://github.com/psf/requests/issues/3490
.venv\Lib\site-packages\pip\_vendor\requests\sessions.py:378: # https://tools.ietf.org/html/rfc7231#section-6.4.4
.venv\Lib\site-packages\pip\_vendor\requests\sessions.py:404: >>> s.get('https://httpbin.org/get')
.venv\Lib\site-packages\pip\_vendor\requests\sessions.py:410: ...     s.get('https://httpbin.org/get')
.venv\Lib\site-packages\pip\_vendor\requests\sessions.py:453: #: (e.g. {'http': 'foo.bar:3128', 'http://host.name': 'foo.bar:4012'}) to
.venv\Lib\site-packages\pip\_vendor\requests\sessions.py:502: self.mount("https://", HTTPAdapter())
.venv\Lib\site-packages\pip\_vendor\requests\sessions.py:503: self.mount("http://", HTTPAdapter())
.venv\Lib\site-packages\pip\_vendor\requests\utils.py:54: proxy_bypass_environment,  # type: ignore[attr-defined]  # https://github.com/python/cpython/issues/145331
.venv\Lib\site-packages\pip\_vendor\requests\utils.py:590: # Assume UTF-8 based on RFC 4627: https://www.ietf.org/rfc/rfc4627.txt since the charset was unset
.venv\Lib\site-packages\pip\_vendor\requests\utils.py:968: i.e. Link: <http:/.../front.jpeg>; rel=front; type="image/jpeg",<http://.../back.jpeg>; rel=back;type="image/jpeg"
.venv\Lib\site-packages\pip\_vendor\requests\__init__.py:14: >>> r = requests.get('https://www.python.org')
.venv\Lib\site-packages\pip\_vendor\requests\__init__.py:23: >>> r = requests.post('https://httpbin.org/post', data=payload)
.venv\Lib\site-packages\pip\_vendor\requests\__init__.py:35: is at <https://requests.readthedocs.io>.
.venv\Lib\site-packages\pip\_vendor\requests\__version__.py:7: __url__ = "https://requests.readthedocs.io"
.venv\Lib\site-packages\pip\_vendor\rich\console.py:969: # https://force-color.org/
.venv\Lib\site-packages\pip\_vendor\rich\console.py:2020: See https://docs.python.org/3/library/signal.html#note-on-sigpipe for details.
.venv\Lib\site-packages\pip\_vendor\rich\console.py:2078: # https://bugs.python.org/issue37871
.venv\Lib\site-packages\pip\_vendor\rich\console.py:2079: # https://github.com/python/cpython/issues/82052
.venv\Lib\site-packages\pip\_vendor\rich\filesize.py:1: """Functions for reporting filesizes. Borrowed from https://github.com/PyFilesystem/pyfilesystem2
.venv\Lib\site-packages\pip\_vendor\rich\filesize.py:9: * `Wikipedia: Binary prefix <https://en.wikipedia.org/wiki/Binary_prefix>`_
.venv\Lib\site-packages\pip\_vendor\rich\highlighter.py:145: Regex reference: https://www.oreilly.com/library/view/regular-expressions-cookbook/9781449327453/ch04s07.html
.venv\Lib\site-packages\pip\_vendor\rich\highlighter.py:221: console.print("https://example.org?foo=bar#header")
.venv\Lib\site-packages\pip\_vendor\rich\logging.py:256: log.info("Listening on http://127.0.0.1:8080")
.venv\Lib\site-packages\pip\_vendor\rich\markup.py:239: "Click [link=https://www.willmcgugan.com]here[/link] to visit my Blog",
.venv\Lib\site-packages\pip\_vendor\rich\progress.py:808: # Based on https://github.com/tqdm/tqdm/blob/master/tqdm/std.py
.venv\Lib\site-packages\pip\_vendor\rich\syntax.py:59: # The following styles are based on https://github.com/pygments/pygments/blob/master/pygments/formatters/terminal.py
.venv\Lib\site-packages\pip\_vendor\rich\syntax.py:245: lexer (Lexer | str): Lexer to use (see https://pygments.org/docs/lexers/)
.venv\Lib\site-packages\pip\_vendor\rich\syntax.py:246: theme (str, optional): Color theme, aka Pygments style (see https://pygments.org/docs/styles/#getting-a-list-of-available-styles). Defaults to "monokai".
.venv\Lib\site-packages\pip\_vendor\rich\syntax.py:341: theme (str, optional): Color theme, aka Pygments style (see https://pygments.org/docs/styles/#getting-a-list-of-available-styles). Defaults to "emacs".
.venv\Lib\site-packages\pip\_vendor\rich\_export_format.py:21: <svg class="rich-terminal" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">
.venv\Lib\site-packages\pip\_vendor\rich\_export_format.py:22: <!-- Generated with Rich https://www.textualize.io -->
.venv\Lib\site-packages\pip\_vendor\rich\_export_format.py:28: url("https://cdnjs.cloudflare.com/ajax/libs/firacode/6.2.0/woff2/FiraCode-Regular.woff2") format("woff2"),
.venv\Lib\site-packages\pip\_vendor\rich\_export_format.py:29: url("https://cdnjs.cloudflare.com/ajax/libs/firacode/6.2.0/woff/FiraCode-Regular.woff") format("woff");
.venv\Lib\site-packages\pip\_vendor\rich\_export_format.py:36: url("https://cdnjs.cloudflare.com/ajax/libs/firacode/6.2.0/woff2/FiraCode-Bold.woff2") format("woff2"),
.venv\Lib\site-packages\pip\_vendor\rich\_export_format.py:37: url("https://cdnjs.cloudflare.com/ajax/libs/firacode/6.2.0/woff/FiraCode-Bold.woff") format("woff");
.venv\Lib\site-packages\pip\_vendor\rich\_palettes.py:4: # Taken from https://en.wikipedia.org/wiki/ANSI_escape_code (Windows 10 column)
.venv\Lib\site-packages\pip\_vendor\rich\_win32_console.py:3: The API that this module wraps is documented at https://docs.microsoft.com/en-us/windows/console/console-functions
.venv\Lib\site-packages\pip\_vendor\rich\_win32_console.py:107: https://docs.microsoft.com/en-us/windows/console/getconsolemode#parameters
.venv\Lib\site-packages\pip\_vendor\rich\__main__.py:241: "https://github.com/sponsors/willmcgugan",
.venv\Lib\site-packages\pip\_vendor\tomli\_parser.py:30: # https://mypyc.readthedocs.io/en/latest/differences_from_python.html#stack-overflows
.venv\Lib\site-packages\pip\_vendor\truststore\_api.py:51: # also see https://github.com/psf/requests/pull/6667
.venv\Lib\site-packages\pip\_vendor\truststore\_macos.py:484: # See: https://github.com/xybp888/iOS-SDKs/blob/master/iPhoneOS13.0.sdk/System/Library/Frameworks/Security.framework/Headers/SecTrust.h#L84
.venv\Lib\site-packages\pip\_vendor\truststore\_openssl.py:7: # candidates based on https://github.com/tiran/certifi-system-store by Christian Heimes
.venv\Lib\site-packages\pip\_vendor\urllib3\connection.py:251: # https://github.com/python/cpython/commit/0d4026432591d43185568dd31cef6a034c4b9261
.venv\Lib\site-packages\pip\_vendor\urllib3\connection.py:252: # and https://github.com/python/cpython/commit/6fbc61070fda2ffb8889e77e3b24bca4249ab4d1
.venv\Lib\site-packages\pip\_vendor\urllib3\connection.py:295: # https://github.com/python/cpython/commit/23aef575c7629abcd4aaf028ebd226fb41a4b3c8
.venv\Lib\site-packages\pip\_vendor\urllib3\connection.py:845: # See: https://github.com/urllib3/urllib3/issues/3267.
.venv\Lib\site-packages\pip\_vendor\urllib3\connection.py:947: # hostnames easily: https://github.com/pyca/pyopenssl/pull/933
.venv\Lib\site-packages\pip\_vendor\urllib3\connection.py:1065: "https://urllib3.readthedocs.io/en/latest/advanced-usage.html"
.venv\Lib\site-packages\pip\_vendor\urllib3\connectionpool.py:116: # This is taken from http://hg.python.org/cpython/file/7aaba721ebc0/Lib/socket.py#l252
.venv\Lib\site-packages\pip\_vendor\urllib3\connectionpool.py:512: # https://erickt.github.io/blog/2014/11/19/adventures-in-debugging-a-potential-osx-kernel-bug/
.venv\Lib\site-packages\pip\_vendor\urllib3\connectionpool.py:738: # [1] <https://github.com/urllib3/urllib3/issues/651>
.venv\Lib\site-packages\pip\_vendor\urllib3\connectionpool.py:1108: # TODO revise this, see https://github.com/urllib3/urllib3/issues/2791
.venv\Lib\site-packages\pip\_vendor\urllib3\connectionpool.py:1114: "https://urllib3.readthedocs.io/en/latest/advanced-usage.html"
.venv\Lib\site-packages\pip\_vendor\urllib3\connectionpool.py:1138: >>> conn = connection_from_url('http://google.com/')
.venv\Lib\site-packages\pip\_vendor\urllib3\connectionpool.py:1170: # *assert* that.  See http://bugs.python.org/issue28539
.venv\Lib\site-packages\pip\_vendor\urllib3\exceptions.py:314: message = "Proxy URL had no scheme, should start with http:// or https://"
.venv\Lib\site-packages\pip\_vendor\urllib3\fields.py:38: `RFC 2388 Section 4.4 <https://tools.ietf.org/html/rfc2388#section-4.4>`_.
.venv\Lib\site-packages\pip\_vendor\urllib3\fields.py:89: https://html.spec.whatwg.org/multipage/
.venv\Lib\site-packages\pip\_vendor\urllib3\poolmanager.py:187: resp1 = http.request("GET", "https://google.com/")
.venv\Lib\site-packages\pip\_vendor\urllib3\poolmanager.py:188: resp2 = http.request("GET", "https://google.com/mail")
.venv\Lib\site-packages\pip\_vendor\urllib3\poolmanager.py:189: resp3 = http.request("GET", "https://yahoo.com/")
.venv\Lib\site-packages\pip\_vendor\urllib3\poolmanager.py:438: "URLs without a scheme (ie 'https://') are deprecated and will raise an error "
.venv\Lib\site-packages\pip\_vendor\urllib3\poolmanager.py:440: "start with 'https://' or 'http://'. Read more in this issue: "
.venv\Lib\site-packages\pip\_vendor\urllib3\poolmanager.py:441: "https://github.com/urllib3/urllib3/issues/2920",
.venv\Lib\site-packages\pip\_vendor\urllib3\poolmanager.py:545: proxy = urllib3.ProxyManager("https://localhost:3128/")
.venv\Lib\site-packages\pip\_vendor\urllib3\poolmanager.py:547: resp1 = proxy.request("GET", "http://google.com/")
.venv\Lib\site-packages\pip\_vendor\urllib3\poolmanager.py:548: resp2 = proxy.request("GET", "http://httpbin.org/")
.venv\Lib\site-packages\pip\_vendor\urllib3\poolmanager.py:554: resp3 = proxy.request("GET", "https://httpbin.org/")
.venv\Lib\site-packages\pip\_vendor\urllib3\poolmanager.py:555: resp4 = proxy.request("GET", "https://twitter.com/")
.venv\Lib\site-packages\pip\_vendor\urllib3\response.py:516: `RFC 8529 Section 8.1 <https://www.rfc-editor.org/rfc/rfc8259#section-8.1>`_.
.venv\Lib\site-packages\pip\_vendor\urllib3\response.py:1023: # December 15, 2012 (http://bugs.python.org/issue16298) do
.venv\Lib\site-packages\pip\_vendor\urllib3\response.py:1044: # See https://github.com/python/cpython/issues/113199
.venv\Lib\site-packages\pip\_vendor\urllib3\__init__.py:38: "See: https://github.com/urllib3/urllib3/issues/3020",
.venv\Lib\site-packages\pip\_vendor\urllib3\__init__.py:45: "See: https://github.com/urllib3/urllib3/issues/2168"
.venv\Lib\site-packages\pip\_vendor\urllib3\contrib\pyopenssl.py:36: .. _pyopenssl: https://www.pyopenssl.org
.venv\Lib\site-packages\pip\_vendor\urllib3\contrib\pyopenssl.py:37: .. _cryptography: https://cryptography.io
.venv\Lib\site-packages\pip\_vendor\urllib3\contrib\pyopenssl.py:38: .. _idna: https://github.com/kjd/idna
.venv\Lib\site-packages\pip\_vendor\urllib3\contrib\socks.py:54: "https://urllib3.readthedocs.io/en/latest/advanced-usage.html#socks-proxies"
.venv\Lib\site-packages\pip\_vendor\urllib3\contrib\socks.py:144: else:  # Defensive: see https://github.com/urllib3/urllib3/pull/3728#pullrequestreview-3816302703
.venv\Lib\site-packages\pip\_vendor\urllib3\contrib\emscripten\fetch.py:7: https://github.com/WebAssembly/js-promise-integration/blob/main/proposals/js-promise-integration/Overview.md
.venv\Lib\site-packages\pip\_vendor\urllib3\contrib\emscripten\fetch.py:61: See also https://github.com/koenvo/pyodide-http/issues/22
.venv\Lib\site-packages\pip\_vendor\urllib3\contrib\emscripten\fetch.py:576: # https://stackoverflow.com/a/78524615
.venv\Lib\site-packages\pip\_vendor\urllib3\contrib\emscripten\response.py:214: `RFC 8529 Section 8.1 <https://www.rfc-editor.org/rfc/rfc8259#section-8.1>`_.
.venv\Lib\site-packages\pip\_vendor\urllib3\http2\connection.py:33: include uppercase characters." (https://httpwg.org/specs/rfc9113.html#n-field-validity)
.venv\Lib\site-packages\pip\_vendor\urllib3\http2\connection.py:49: 0x20 or 0x09)." (https://httpwg.org/specs/rfc9113.html#n-field-validity)
.venv\Lib\site-packages\pip\_vendor\urllib3\http2\__init__.py:22: "See: https://github.com/urllib3/urllib3/issues/3290"
.venv\Lib\site-packages\pip\_vendor\urllib3\util\connection.py:123: # https://github.com/urllib3/urllib3/pull/611
.venv\Lib\site-packages\pip\_vendor\urllib3\util\connection.py:124: # https://bugs.python.org/issue658327
.venv\Lib\site-packages\pip\_vendor\urllib3\util\response.py:72: # See: https://github.com/urllib3/urllib3/issues/800
.venv\Lib\site-packages\pip\_vendor\urllib3\util\retry.py:53: response = http.request("GET", "https://example.com/")
.venv\Lib\site-packages\pip\_vendor\urllib3\util\retry.py:59: response = http.request("GET", "https://example.com/", retries=Retry(10))
.venv\Lib\site-packages\pip\_vendor\urllib3\util\retry.py:65: response = http.request("GET", "https://example.com/", retries=False)
.venv\Lib\site-packages\pip\_vendor\urllib3\util\retry.py:330: # Whitespace: https://tools.ietf.org/html/rfc7230#section-3.2.4
.venv\Lib\site-packages\pip\_vendor\urllib3\util\ssl_.py:34: # only common names, see https://github.com/urllib3/urllib3/pull/3024
.venv\Lib\site-packages\pip\_vendor\urllib3\util\ssl_match_hostname.py:4: # stdlib.   http://docs.python.org/3/license.html
.venv\Lib\site-packages\pip\_vendor\urllib3\util\ssl_match_hostname.py:29: http://tools.ietf.org/html/rfc6125#section-6.4.3
.venv\Lib\site-packages\pip\_vendor\urllib3\util\timeout.py:38: resp = http.request("GET", "https://example.com/")
.venv\Lib\site-packages\pip\_vendor\urllib3\util\timeout.py:46: response = http.request("GET", "https://example.com/", timeout=Timeout(10))
.venv\Lib\site-packages\pip\_vendor\urllib3\util\timeout.py:53: response = http.request("GET", "https://example.com/", timeout=no_timeout)
.venv\Lib\site-packages\pip\_vendor\urllib3\util\timeout.py:71: <http://hg.python.org/cpython/file/603b4d593758/Lib/socket.py#l535>`_.
.venv\Lib\site-packages\pip\_vendor\urllib3\util\timeout.py:81: <http://hg.python.org/cpython/file/603b4d593758/Lib/socket.py#l535>`_.
.venv\Lib\site-packages\pip\_vendor\urllib3\util\url.py:14: # 'rfc3986' module: https://github.com/python-hyper/rfc3986
.venv\Lib\site-packages\pip\_vendor\urllib3\util\url.py:177: U = urllib3.util.parse_url("https://google.com/mail/")
.venv\Lib\site-packages\pip\_vendor\urllib3\util\url.py:180: # "https://google.com/mail/"
.venv\Lib\site-packages\pip\_vendor\urllib3\util\url.py:186: # "https://username:password@host.com:80/path?query#fragment"
.venv\Lib\site-packages\pip\_vendor\urllib3\util\url.py:264: # See http://tools.ietf.org/html/rfc3986#section-5.2.4 for pseudo-code
.venv\Lib\site-packages\pip\_vendor\urllib3\util\url.py:386: print( urllib3.util.parse_url('http://google.com/mail/'))
.venv\Lib\site-packages\pygame\colordict.py:23: See https://pyga.me/docs/ref/color_list.html for sample swatches.
.venv\Lib\site-packages\pygame\cursors.py:201: # See https://github.com/pygame/pygame/pull/2509 for analysis
.venv\Lib\site-packages\pygame\sysfont.py:80: # https://github.com/pygame-community/pygame-ce/issues/3742
.venv\Lib\site-packages\pygame\__init__.py:317: See https://docs.python.org/3/library/importlib.html#implementing-lazy-imports
.venv\Lib\site-packages\pygame\docs\serve.py:61: print(f"Serving on: http://{TARGET}:{parsed_args.port}")
.venv\Lib\site-packages\pygame\docs\serve.py:64: webbrowser.open(f"http://{TARGET}:{parsed_args.port}")
.venv\Lib\site-packages\pygame\docs\static.py:13: url = "https://pyga.me/docs/"
.venv\Lib\site-packages\pygame\examples\freetype_misc.py:15: https://freetype.org
.venv\Lib\site-packages\pygame\examples\window_opengl.py:3: Slightly modified version of the example at https://github.com/szabolcsdombi/zengl/blob/main/examples/pygame/hello_world.py
.venv\Lib\site-packages\pygame\examples\window_opengl.py:6: Posted here with permission from https://github.com/szabolcsdombi given in the PGC discord server
.venv\Lib\site-packages\pygame\tests\display_test.py:611: # see https://github.com/pygame-community/pygame-ce/issues/1194
.venv\Lib\site-packages\pygame\tests\display_test.py:1003: # Test for https://github.com/pygame-community/pygame-ce/issues/924
.venv\Lib\site-packages\pygame\tests\draw_test.py:3775: See: https://github.com/pygame-community/pygame-ce/pull/2912
.venv\Lib\site-packages\pygame\tests\draw_test.py:3798: See: https://github.com/pygame-community/pygame-ce/pull/2912
.venv\Lib\site-packages\pygame\tests\draw_test.py:5854: see https://github.com/pygame/pygame/issues/3143
.venv\Lib\site-packages\pygame\tests\draw_test.py:5883: https://github.com/pygame-community/pygame-ce/commit/c88a1d8f7b31099cec84dc5cb7aeebdada783e83
.venv\Lib\site-packages\pygame\tests\draw_test.py:6618: see https://github.com/pygame/pygame/issues/3143
.venv\Lib\site-packages\pygame\tests\draw_test.py:6647: https://github.com/pygame-community/pygame-ce/commit/c88a1d8f7b31099cec84dc5cb7aeebdada783e83
.venv\Lib\site-packages\pygame\tests\draw_test.py:6674: see https://github.com/pygame-community/pygame-ce/issues/3682
.venv\Lib\site-packages\pygame\tests\draw_test.py:7526: https://github.com/pygame-community/pygame-ce/pull/3008
.venv\Lib\site-packages\pygame\tests\event_test.py:385: # Ref: https://www.libsdl.org/tmp/SDL/include/SDL_events.h
.venv\Lib\site-packages\pygame\tests\font_test.py:725: # http://www.mail-archive.com/pygame-users@seul.org/msg11675.html
.venv\Lib\site-packages\pygame\tests\freetype_test.py:64: # http://www.levien.com/type/myfonts/inconsolata.html
.venv\Lib\site-packages\pygame\tests\freetype_test.py:69: # https://fedorahosted.org/liberation-fonts/
.venv\Lib\site-packages\pygame\tests\pixelarray_test.py:1309: Regression test for pygame-ce issue 2275 (https://github.com/pygame-community/pygame-ce/issues/2275)
.venv\Lib\site-packages\pygame\tests\pixelarray_test.py:1319: Regression test for https://github.com/pygame-community/pygame-ce/issues/2740
.venv\Lib\site-packages\pygame\tests\surface_test.py:49: # See https://github.com/pygame-community/pygame-ce/issues/796
.venv\Lib\site-packages\pygame\tests\surface_test.py:305: # https://github.com/libsdl-org/sdl2-compat/issues/575
.venv\Lib\site-packages\pygame\tests\surface_test.py:1237: # https://github.com/pygame-community/pygame-ce/issues/146
.venv\Lib\site-packages\pygame\tests\surface_test.py:2524: https://github.com/pygame-community/pygame-ce/issues/541
.venv\Lib\site-packages\pygame\tests\surface_test.py:2635: # Issue https://github.com/pygame-community/pygame-ce/issues/17
.venv\Lib\site-packages\pygame\tests\surface_test.py:4119: This test case is in response to https://github.com/pygame-community/pygame-ce/issues/34
.venv\Lib\site-packages\pygame\tests\surface_test.py:4196: # https://github.com/pygame-community/pygame-ce/issues/374, final comment by illume
.venv\Lib\site-packages\pygame\tests\surface_test.py:4200: # https://github.com/pygame-community/pygame-ce/issues/34
.venv\Lib\site-packages\pygame\tests\surface_test.py:4219: # https://github.com/pygame-community/pygame-ce/issues/374 final comment by illume
.venv\Lib\site-packages\pygame\tests\surface_test.py:4223: # https://github.com/pygame-community/pygame-ce/issues/34
.venv\Lib\site-packages\pygame\tests\surface_test.py:4355: """Regression test for https://github.com/pygame-community/pygame-ce/issues/2938"""
.venv\Lib\site-packages\pygame\tests\transform_test.py:193: https://github.com/pygame-community/pygame-ce/issues/3463"""
.venv\Lib\site-packages\pygame\tests\transform_test.py:1592: # Tests a regression found from https://github.com/pygame-community/pygame-ce/pull/3314
.venv\Lib\site-packages\pygame\tests\transform_test.py:1593: # Reported in https://github.com/pygame-community/pygame-ce/issues/3463
.venv\Lib\site-packages\pygame\tests\transform_test.py:1873: https://github.com/pygame-community/pygame-ce/issues/3463"""
.venv\Lib\site-packages\pygame\tests\test_utils\async_sub.py:4: Modification of http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/440554
.venv\Lib\site-packages\pygame\tests\test_utils\async_sub.py:160: # http://me.in-berlin.de/doc/python/faq/windows.html#how-do-i-emulate-os-kill-in-windows
.venv\Lib\site-packages\pygame\tests\test_utils\async_sub.py:161: # http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/347462
.venv\Lib\site-packages\pygame\tests\test_utils\png.py:3: # $URL: http://pypng.googlecode.com/svn/trunk/code/png.py $
.venv\Lib\site-packages\pygame\tests\test_utils\png.py:52: # http://trac.browsershots.org/browser/trunk/pypng/lib/png.py?rev=2885
.venv\Lib\site-packages\pygame\tests\test_utils\png.py:62: specification at http://www.w3.org/TR/2003/REC-PNG-20031110/ ). It reads
.venv\Lib\site-packages\pygame\tests\test_utils\png.py:75: `Netpbm <http://netpbm.sourceforge.net/>`_ PNM files to PNG, and the reverse conversion from PNG to
.venv\Lib\site-packages\pygame\tests\test_utils\png.py:162: __version__ = "$URL: http://pypng.googlecode.com/svn/trunk/code/png.py $ $Rev: 228 $"
.venv\Lib\site-packages\pygame\tests\test_utils\png.py:181: # http://www.w3.org/TR/PNG/#5PNG-file-signature
.venv\Lib\site-packages\pygame\tests\test_utils\png.py:197: # http://www.python.org/doc/2.6/library/functions.html#zip
.venv\Lib\site-packages\pygame\tests\test_utils\png.py:238: # See http://www.python.org/doc/2.4.4/lib/module-array.html#l2h-1356
.venv\Lib\site-packages\pygame\tests\test_utils\png.py:504: # http://www.w3.org/TR/PNG/#7Integers-and-byte-order
.venv\Lib\site-packages\pygame\tests\test_utils\png.py:655: # http://www.w3.org/TR/PNG/#5PNG-file-signature
.venv\Lib\site-packages\pygame\tests\test_utils\png.py:658: # http://www.w3.org/TR/PNG/#11IHDR
.venv\Lib\site-packages\pygame\tests\test_utils\png.py:675: # http://www.w3.org/TR/PNG/#11gAMA
.venv\Lib\site-packages\pygame\tests\test_utils\png.py:682: # http://www.w3.org/TR/PNG/#11sBIT
.venv\Lib\site-packages\pygame\tests\test_utils\png.py:693: # See http://www.w3.org/TR/PNG/#5ChunkOrdering
.venv\Lib\site-packages\pygame\tests\test_utils\png.py:702: # http://www.w3.org/TR/PNG/#11tRNS
.venv\Lib\site-packages\pygame\tests\test_utils\png.py:709: # http://www.w3.org/TR/PNG/#11bKGD
.venv\Lib\site-packages\pygame\tests\test_utils\png.py:716: # http://www.w3.org/TR/PNG/#11IDAT
.venv\Lib\site-packages\pygame\tests\test_utils\png.py:763: # http://code.google.com/p/pypng/issues/detail?id=44
.venv\Lib\site-packages\pygame\tests\test_utils\png.py:814: # http://www.w3.org/TR/PNG/#11IEND
.venv\Lib\site-packages\pygame\tests\test_utils\png.py:941: # http://www.w3.org/TR/PNG/#8InterlaceMethods
.venv\Lib\site-packages\pygame\tests\test_utils\png.py:975: # http://www.w3.org/TR/PNG/#5Chunk-layout
.venv\Lib\site-packages\pygame\tests\test_utils\png.py:1034: # http://www.w3.org/TR/PNG/#9Filter-type-4-Paeth
.venv\Lib\site-packages\pygame\tests\test_utils\png.py:1414: # http://www.w3.org/TR/PNG/#5Chunk-layout
.venv\Lib\site-packages\pygame\tests\test_utils\png.py:1433: # http://bugs.python.org/issue1202 .
.venv\Lib\site-packages\pygame\tests\test_utils\png.py:1490: "  See http://www.w3.org/TR/2003/REC-PNG-20031110/#9Filters ."
.venv\Lib\site-packages\pygame\tests\test_utils\png.py:1759: # http://www.w3.org/TR/PNG/#11IHDR
.venv\Lib\site-packages\pygame\tests\test_utils\png.py:1786: " See http://www.w3.org/TR/2003/REC-PNG-20031110/#table111 ."
.venv\Lib\site-packages\pygame\tests\test_utils\png.py:1794: " see http://www.w3.org/TR/2003/REC-PNG-20031110/#9Filters ."
.venv\Lib\site-packages\pygame\tests\test_utils\png.py:1800: " see http://www.w3.org/TR/2003/REC-PNG-20031110/#8InterlaceMethods ."
.venv\Lib\site-packages\pygame\tests\test_utils\png.py:1805: # http://www.w3.org/TR/PNG/#6Colour-values
.venv\Lib\site-packages\pygame\tests\test_utils\png.py:1830: # http://www.w3.org/TR/PNG/#11PLTE
.venv\Lib\site-packages\pygame\tests\test_utils\png.py:1851: # http://www.w3.org/TR/PNG/#11tRNS
.venv\Lib\site-packages\pygame\tests\test_utils\png.py:1903: # http://www.w3.org/TR/PNG/#11IEND
.venv\Lib\site-packages\pygame\tests\test_utils\png.py:1908: # http://www.w3.org/TR/PNG/#11IDAT
.venv\Lib\site-packages\pygame\tests\test_utils\png.py:2334: # http://docs.python.org/library/inspect.html#the-interpreter-stack
.venv\Lib\site-packages\pygame\tests\test_utils\png.py:2834: # from http://www.schaik.com/pngsuite/pngsuite_bas_png.html
.venv\Lib\site-packages\pygame\tests\test_utils\png.py:3648: # Generally, see http://netpbm.sourceforge.net/doc/ppm.html
.venv\Lib\site-packages\pygame\tests\test_utils\png.py:3649: # and http://netpbm.sourceforge.net/doc/pam.html
.venv\Lib\site-packages\pygame\tests\test_utils\png.py:3743: # See http://netpbm.sourceforge.net/doc/pam.html
.venv\Lib\site-packages\pygame\tests\test_utils\test_runner.py:289: # https://github.com/python/cpython/pull/114994
.venv\Lib\site-packages\PySide6\QtAsyncio\events.py:108: https://discuss.python.org/t/removing-the-asyncio-policy-system-asyncio-set-event-loop-policy-in-python-3-15/37553
.venv\Lib\site-packages\PySide6\QtAsyncio\events.py:149: https://docs.python.org/3/library/asyncio-eventloop.html
.venv\Lib\site-packages\PySide6\QtAsyncio\events.py:627: # https://docs.python.org/3/library/asyncio-dev.html#asyncio-debug-mode
.venv\Lib\site-packages\PySide6\QtAsyncio\events.py:687: # https://docs.python.org/3/library/asyncio-dev.html#asyncio-multithreading
.venv\Lib\site-packages\PySide6\QtAsyncio\futures.py:16: """ https://docs.python.org/3/library/asyncio-future.html """
.venv\Lib\site-packages\PySide6\QtAsyncio\tasks.py:19: """ https://docs.python.org/3/library/asyncio-task.html """
.venv\Lib\site-packages\PySide6\QtAsyncio\tasks.py:50: # https://docs.python.org/3/library/asyncio-extending.html#task-lifetime-support
.venv\Lib\site-packages\PySide6\QtAsyncio\tasks.py:179: # https://docs.python.org/3/library/asyncio-extending.html#task-lifetime-support
.venv\Lib\site-packages\PySide6\QtAsyncio\__init__.py:59: # https://discuss.python.org/t/removing-the-asyncio-policy-system-asyncio-set-event-loop-policy-in-python-3-15/37553  # noqa: E501
.venv\Lib\site-packages\PySide6\scripts\deploy.py:127: # Nuitka Issue: https://github.com/Nuitka/Nuitka/issues/3079
.venv\Lib\site-packages\PySide6\scripts\project.py:22: https://doc.qt.io/qtforpython-6/tools/pyside-project.html
.venv\Lib\site-packages\PySide6\scripts\pyside_tool.py:161: # https://www.python.org/dev/peps/pep-0384/#linkage :
.venv\Lib\site-packages\PySide6\scripts\pyside_tool.py:167: # https://stackoverflow.com/questions/49784583/numpy-import-fails-on-multiarray-extension-library-when-called-from-embedded-pyt
.venv\Lib\site-packages\PySide6\scripts\deploy_lib\nuitka_helper.py:60: # https://nuitka.net/user-documentation/user-manual.html#nuitka-project-options
.venv\Lib\site-packages\requests\adapters.py:182: >>> s.mount('http://', a)
.venv\Lib\site-packages\requests\adapters.py:531: "https://github.com/psf/requests/pull/6710 for more details."
.venv\Lib\site-packages\requests\api.py:62: >>> req = requests.request('GET', 'https://httpbin.org/get')
.venv\Lib\site-packages\requests\auth.py:281: # See https://github.com/psf/requests/issues/3772
.venv\Lib\site-packages\requests\compat.py:105: proxy_bypass_environment,  # type: ignore[attr-defined]  # https://github.com/python/cpython/issues/145331
.venv\Lib\site-packages\requests\models.py:14: # such as in Embedded Python. See https://github.com/psf/requests/issues/3578.
.venv\Lib\site-packages\requests\models.py:306: >>> req = requests.Request('GET', 'https://httpbin.org/get')
.venv\Lib\site-packages\requests\models.py:387: >>> req = requests.Request('GET', 'https://httpbin.org/get')
.venv\Lib\site-packages\requests\models.py:491: #: https://github.com/psf/requests/pull/2238
.venv\Lib\site-packages\requests\models.py:516: f"Perhaps you meant https://{url}?"
.venv\Lib\site-packages\requests\sessions.py:238: # (e.g. '/path/to/resource' instead of 'http://domain.tld/path/to/resource')
.venv\Lib\site-packages\requests\sessions.py:249: # https://github.com/psf/requests/issues/1084
.venv\Lib\site-packages\requests\sessions.py:254: # https://github.com/psf/requests/issues/3490
.venv\Lib\site-packages\requests\sessions.py:378: # https://tools.ietf.org/html/rfc7231#section-6.4.4
.venv\Lib\site-packages\requests\sessions.py:404: >>> s.get('https://httpbin.org/get')
.venv\Lib\site-packages\requests\sessions.py:410: ...     s.get('https://httpbin.org/get')
.venv\Lib\site-packages\requests\sessions.py:453: #: (e.g. {'http': 'foo.bar:3128', 'http://host.name': 'foo.bar:4012'}) to
.venv\Lib\site-packages\requests\sessions.py:502: self.mount("https://", HTTPAdapter())
.venv\Lib\site-packages\requests\sessions.py:503: self.mount("http://", HTTPAdapter())
.venv\Lib\site-packages\requests\utils.py:54: proxy_bypass_environment,  # type: ignore[attr-defined]  # https://github.com/python/cpython/issues/145331
.venv\Lib\site-packages\requests\utils.py:590: # Assume UTF-8 based on RFC 4627: https://www.ietf.org/rfc/rfc4627.txt since the charset was unset
.venv\Lib\site-packages\requests\utils.py:968: i.e. Link: <http:/.../front.jpeg>; rel=front; type="image/jpeg",<http://.../back.jpeg>; rel=back;type="image/jpeg"
.venv\Lib\site-packages\requests\__init__.py:14: >>> r = requests.get('https://www.python.org')
.venv\Lib\site-packages\requests\__init__.py:23: >>> r = requests.post('https://httpbin.org/post', data=payload)
.venv\Lib\site-packages\requests\__init__.py:35: is at <https://requests.readthedocs.io>.
.venv\Lib\site-packages\requests\__version__.py:7: __url__ = "https://requests.readthedocs.io"
.venv\Lib\site-packages\urllib3\connection.py:251: # https://github.com/python/cpython/commit/0d4026432591d43185568dd31cef6a034c4b9261
.venv\Lib\site-packages\urllib3\connection.py:252: # and https://github.com/python/cpython/commit/6fbc61070fda2ffb8889e77e3b24bca4249ab4d1
.venv\Lib\site-packages\urllib3\connection.py:295: # https://github.com/python/cpython/commit/23aef575c7629abcd4aaf028ebd226fb41a4b3c8
.venv\Lib\site-packages\urllib3\connection.py:845: # See: https://github.com/urllib3/urllib3/issues/3267.
.venv\Lib\site-packages\urllib3\connection.py:947: # hostnames easily: https://github.com/pyca/pyopenssl/pull/933
.venv\Lib\site-packages\urllib3\connection.py:1065: "https://urllib3.readthedocs.io/en/latest/advanced-usage.html"
.venv\Lib\site-packages\urllib3\connectionpool.py:116: # This is taken from http://hg.python.org/cpython/file/7aaba721ebc0/Lib/socket.py#l252
.venv\Lib\site-packages\urllib3\connectionpool.py:512: # https://erickt.github.io/blog/2014/11/19/adventures-in-debugging-a-potential-osx-kernel-bug/
.venv\Lib\site-packages\urllib3\connectionpool.py:738: # [1] <https://github.com/urllib3/urllib3/issues/651>
.venv\Lib\site-packages\urllib3\connectionpool.py:1108: # TODO revise this, see https://github.com/urllib3/urllib3/issues/2791
.venv\Lib\site-packages\urllib3\connectionpool.py:1114: "https://urllib3.readthedocs.io/en/latest/advanced-usage.html"
.venv\Lib\site-packages\urllib3\connectionpool.py:1138: >>> conn = connection_from_url('http://google.com/')
.venv\Lib\site-packages\urllib3\connectionpool.py:1170: # *assert* that.  See http://bugs.python.org/issue28539
.venv\Lib\site-packages\urllib3\exceptions.py:314: message = "Proxy URL had no scheme, should start with http:// or https://"
.venv\Lib\site-packages\urllib3\exceptions.py:316: message = f"Proxy URL had unsupported scheme {scheme}, should use http:// or https://"
.venv\Lib\site-packages\urllib3\fields.py:38: `RFC 2388 Section 4.4 <https://tools.ietf.org/html/rfc2388#section-4.4>`_.
.venv\Lib\site-packages\urllib3\fields.py:89: https://html.spec.whatwg.org/multipage/
.venv\Lib\site-packages\urllib3\poolmanager.py:187: resp1 = http.request("GET", "https://google.com/")
.venv\Lib\site-packages\urllib3\poolmanager.py:188: resp2 = http.request("GET", "https://google.com/mail")
.venv\Lib\site-packages\urllib3\poolmanager.py:189: resp3 = http.request("GET", "https://yahoo.com/")
.venv\Lib\site-packages\urllib3\poolmanager.py:438: "URLs without a scheme (ie 'https://') are deprecated and will raise an error "
.venv\Lib\site-packages\urllib3\poolmanager.py:440: "start with 'https://' or 'http://'. Read more in this issue: "
.venv\Lib\site-packages\urllib3\poolmanager.py:441: "https://github.com/urllib3/urllib3/issues/2920",
.venv\Lib\site-packages\urllib3\poolmanager.py:545: proxy = urllib3.ProxyManager("https://localhost:3128/")
.venv\Lib\site-packages\urllib3\poolmanager.py:547: resp1 = proxy.request("GET", "http://google.com/")
.venv\Lib\site-packages\urllib3\poolmanager.py:548: resp2 = proxy.request("GET", "http://httpbin.org/")
.venv\Lib\site-packages\urllib3\poolmanager.py:554: resp3 = proxy.request("GET", "https://httpbin.org/")
.venv\Lib\site-packages\urllib3\poolmanager.py:555: resp4 = proxy.request("GET", "https://twitter.com/")
.venv\Lib\site-packages\urllib3\response.py:522: `RFC 8529 Section 8.1 <https://www.rfc-editor.org/rfc/rfc8259#section-8.1>`_.
.venv\Lib\site-packages\urllib3\response.py:1029: # December 15, 2012 (http://bugs.python.org/issue16298) do
.venv\Lib\site-packages\urllib3\response.py:1050: # See https://github.com/python/cpython/issues/113199
.venv\Lib\site-packages\urllib3\__init__.py:38: "See: https://github.com/urllib3/urllib3/issues/3020",
.venv\Lib\site-packages\urllib3\__init__.py:45: "See: https://github.com/urllib3/urllib3/issues/2168"
.venv\Lib\site-packages\urllib3\contrib\pyopenssl.py:36: .. _pyopenssl: https://www.pyopenssl.org
.venv\Lib\site-packages\urllib3\contrib\pyopenssl.py:37: .. _cryptography: https://cryptography.io
.venv\Lib\site-packages\urllib3\contrib\pyopenssl.py:38: .. _idna: https://github.com/kjd/idna
.venv\Lib\site-packages\urllib3\contrib\socks.py:54: "https://urllib3.readthedocs.io/en/latest/advanced-usage.html#socks-proxies"
.venv\Lib\site-packages\urllib3\contrib\socks.py:144: else:  # Defensive: see https://github.com/urllib3/urllib3/pull/3728#pullrequestreview-3816302703
.venv\Lib\site-packages\urllib3\contrib\emscripten\fetch.py:7: https://github.com/WebAssembly/js-promise-integration/blob/main/proposals/js-promise-integration/Overview.md
.venv\Lib\site-packages\urllib3\contrib\emscripten\fetch.py:61: See also https://github.com/koenvo/pyodide-http/issues/22
.venv\Lib\site-packages\urllib3\contrib\emscripten\fetch.py:576: # https://stackoverflow.com/a/78524615
.venv\Lib\site-packages\urllib3\contrib\emscripten\response.py:214: `RFC 8529 Section 8.1 <https://www.rfc-editor.org/rfc/rfc8259#section-8.1>`_.
.venv\Lib\site-packages\urllib3\http2\connection.py:33: include uppercase characters." (https://httpwg.org/specs/rfc9113.html#n-field-validity)
.venv\Lib\site-packages\urllib3\http2\connection.py:49: 0x20 or 0x09)." (https://httpwg.org/specs/rfc9113.html#n-field-validity)
.venv\Lib\site-packages\urllib3\http2\__init__.py:22: "See: https://github.com/urllib3/urllib3/issues/3290"
.venv\Lib\site-packages\urllib3\util\connection.py:123: # https://github.com/urllib3/urllib3/pull/611
.venv\Lib\site-packages\urllib3\util\connection.py:124: # https://bugs.python.org/issue658327
.venv\Lib\site-packages\urllib3\util\response.py:72: # See: https://github.com/urllib3/urllib3/issues/800
.venv\Lib\site-packages\urllib3\util\retry.py:53: response = http.request("GET", "https://example.com/")
.venv\Lib\site-packages\urllib3\util\retry.py:59: response = http.request("GET", "https://example.com/", retries=Retry(10))
.venv\Lib\site-packages\urllib3\util\retry.py:65: response = http.request("GET", "https://example.com/", retries=False)
.venv\Lib\site-packages\urllib3\util\retry.py:330: # Whitespace: https://tools.ietf.org/html/rfc7230#section-3.2.4
.venv\Lib\site-packages\urllib3\util\ssl_.py:34: # only common names, see https://github.com/urllib3/urllib3/pull/3024
.venv\Lib\site-packages\urllib3\util\ssl_match_hostname.py:4: # stdlib.   http://docs.python.org/3/license.html
.venv\Lib\site-packages\urllib3\util\ssl_match_hostname.py:29: http://tools.ietf.org/html/rfc6125#section-6.4.3
.venv\Lib\site-packages\urllib3\util\timeout.py:38: resp = http.request("GET", "https://example.com/")
.venv\Lib\site-packages\urllib3\util\timeout.py:46: response = http.request("GET", "https://example.com/", timeout=Timeout(10))
.venv\Lib\site-packages\urllib3\util\timeout.py:53: response = http.request("GET", "https://example.com/", timeout=no_timeout)
.venv\Lib\site-packages\urllib3\util\timeout.py:71: <http://hg.python.org/cpython/file/603b4d593758/Lib/socket.py#l535>`_.
.venv\Lib\site-packages\urllib3\util\timeout.py:81: <http://hg.python.org/cpython/file/603b4d593758/Lib/socket.py#l535>`_.
.venv\Lib\site-packages\urllib3\util\url.py:14: # 'rfc3986' module: https://github.com/python-hyper/rfc3986
.venv\Lib\site-packages\urllib3\util\url.py:177: U = urllib3.util.parse_url("https://google.com/mail/")
.venv\Lib\site-packages\urllib3\util\url.py:180: # "https://google.com/mail/"
.venv\Lib\site-packages\urllib3\util\url.py:186: # "https://username:password@host.com:80/path?query#fragment"
.venv\Lib\site-packages\urllib3\util\url.py:264: # See http://tools.ietf.org/html/rfc3986#section-5.2.4 for pseudo-code
.venv\Lib\site-packages\urllib3\util\url.py:386: print( urllib3.util.parse_url('http://google.com/mail/'))
core\steam_enricher.py:52: url_search = f"https://store.steampowered.com/api/storesearch/?term={urllib.parse.quote(titulo_limpio)}&l=spanish&cc=ES"
core\steam_enricher.py:67: banner_url = f"https://cdn.akamai.steamstatic.com/steam/apps/{appid}/header.jpg"
core\steam_enricher.py:69: url_reviews = f"https://store.steampowered.com/appreviews/{appid}?json=1&language=all&purchase_type=all"
core\steam_enricher.py:139: cached["banner_url"] = f"https://cdn.akamai.steamstatic.com/steam/apps/{cached['appid']}/header.jpg"
core\translator.py:32: url_google = f"https://translate.google.com/m?sl=auto&tl={target_lang}&q={urllib.parse.quote(texto)}"
core\translator.py:49: url_mm = f"https://api.mymemory.translated.net/get?q={urllib.parse.quote(texto[:450])}&langpair=en|{target_lang}"
core\scrapers\store_scrapers.py:27: _session_scrapers.mount("https://", adapter)
core\scrapers\store_scrapers.py:28: _session_scrapers.mount("http://", adapter)
core\scrapers\store_scrapers.py:93: url = "https://store-site-backend-static.ak.epicgames.com/freeGamesPromotions?locale=es-ES&country=ES"
core\scrapers\store_scrapers.py:157: giveaway_url = f"https://store.epicgames.com/es-ES/p/{slug}" if slug else "https://store.epicgames.com/free-games"
core\scrapers\store_scrapers.py:184: url = "https://store.steampowered.com/api/featuredcategories"
core\scrapers\store_scrapers.py:206: "open_giveaway_url": f"https://store.steampowered.com/app/{it.get('id')}/",
core\scrapers\store_scrapers.py:221: url = "https://itch.io/games/on-sale?format=json"
core\scrapers\store_scrapers.py:241: url_juego = urllib.parse.urljoin("https://itch.io", url_raw)
core\scrapers\store_scrapers.py:254: imagen = urllib.parse.urljoin("https://itch.io", imagen)
core\scrapers\store_scrapers.py:287: url = "https://catalog.gog.com/v1/catalog?limit=48&order=desc:bestselling&discounted=eq:true"
core\scrapers\store_scrapers.py:310: link = p.get("storeLink") or f"https://www.gog.com/game/{slug}"
tests\test_history.py:93: url_juego = urllib.parse.urljoin("https://itch.io", title_m.group(1).strip())
tests\test_history.py:96: self.assertEqual(url_juego, "https://itch.io/games/retro-quest")
tests\test_integration_e2e.py:32: self.assertTrue(es_url_segura("https://store.epicgames.com/p/free-game"))
tests\test_integration_e2e.py:33: self.assertFalse(es_url_segura("http://insecure-http-site.com"))
tests\test_phase2_p1.py:11: "https://store.steampowered.com/app/123456/",
tests\test_phase2_p1.py:12: "https://store.epicgames.com/p/game-title",
tests\test_phase2_p1.py:13: "https://www.gog.com/game/title",
tests\test_phase2_p1.py:14: "https://itch.io/games/free",
tests\test_phase2_p1.py:15: "https://ko-fi.com/project",
tests\test_phase2_p1.py:23: "http://store.steampowered.com/app/123456/",  # HTTP rechazado
tests\test_phase2_p1.py:26: "https://evil-phishing-site.com/steam",       # Dominio no autorizado
tests\test_phase2_p1.py:27: "https://steampowered.com.attacker.com/",     # Subdominio trampa
tests\test_phase2_p1.py:34: self.assertIsNone(descargar_contenido_seguro("http://example.com/image.png"))
ui\modals\kofi_modal.py:82: webbrowser.open_new_tab("https://ko-fi.com")
```

### Network pattern: requests\.

```text
.venv\Lib\site-packages\pip\_internal\exceptions.py:33: from pip._vendor.requests.models import PreparedRequest, Request, Response
.venv\Lib\site-packages\pip\_internal\cli\index_command.py:81: # there's no type annotation on requests.Session, so it's
.venv\Lib\site-packages\pip\_internal\commands\install.py:18: from pip._vendor.requests.exceptions import InvalidProxyURL
.venv\Lib\site-packages\pip\_internal\distributions\sdist.py:149: # Install any extra build dependencies that the backend requests.
.venv\Lib\site-packages\pip\_internal\index\collector.py:416: :param session: The Session to use to make requests.
.venv\Lib\site-packages\pip\_internal\network\auth.py:4: providing credentials in the context of network requests.
.venv\Lib\site-packages\pip\_internal\network\auth.py:23: from pip._vendor.requests.auth import AuthBase, HTTPBasicAuth
.venv\Lib\site-packages\pip\_internal\network\auth.py:24: from pip._vendor.requests.utils import get_netrc_auth
.venv\Lib\site-packages\pip\_internal\network\auth.py:38: from pip._vendor.requests.models import Response
.venv\Lib\site-packages\pip\_internal\network\cache.py:14: from pip._vendor.requests.models import Response
.venv\Lib\site-packages\pip\_internal\network\download.py:15: from pip._vendor.requests.models import Response
.venv\Lib\site-packages\pip\_internal\network\download.py:288: #   requests.request() connection exception handler.
.venv\Lib\site-packages\pip\_internal\network\lazy_wheel.py:15: from pip._vendor.requests.models import CONTENT_CHUNK_SIZE, Response
.venv\Lib\site-packages\pip\_internal\network\session.py:29: from pip._vendor.requests.adapters import DEFAULT_POOLBLOCK, BaseAdapter
.venv\Lib\site-packages\pip\_internal\network\session.py:32: from pip._vendor.requests.structures import CaseInsensitiveDict
.venv\Lib\site-packages\pip\_internal\network\session.py:306: class PipSession(requests.Session):
.venv\Lib\site-packages\pip\_internal\network\session.py:523: except (requests.ConnectionError, requests.Timeout) as e:
.venv\Lib\site-packages\pip\_internal\network\utils.py:6: from pip._vendor.requests.models import Response
.venv\Lib\site-packages\pip\_internal\network\utils.py:155: error: requests.ConnectionError | requests.Timeout,
.venv\Lib\site-packages\pip\_internal\network\utils.py:162: Note: requests.ConnectionError is the parent class of
.venv\Lib\site-packages\pip\_internal\network\utils.py:163: requests.ProxyError, requests.SSLError, and requests.ConnectTimeout
.venv\Lib\site-packages\pip\_internal\vcs\subversion.py:161: # are only potentially needed for remote server requests.
.venv\Lib\site-packages\pip\_vendor\__init__.py:74: vendored("requests.exceptions")
.venv\Lib\site-packages\pip\_vendor\__init__.py:75: vendored("requests.packages")
.venv\Lib\site-packages\pip\_vendor\__init__.py:76: vendored("requests.packages.urllib3")
.venv\Lib\site-packages\pip\_vendor\__init__.py:77: vendored("requests.packages.urllib3._collections")
.venv\Lib\site-packages\pip\_vendor\__init__.py:78: vendored("requests.packages.urllib3.connection")
