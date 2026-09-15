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
.venv\Lib\site-packages\numpy\_core\tests\test_multiarray.py:4454: MyType = eval("type('MyType', (base,), class_namespace)",
.venv\Lib\site-packages\numpy\_core\tests\test_records.py:184: recordarr_r = eval("np." + repr(recordarr), {'np': np})
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

