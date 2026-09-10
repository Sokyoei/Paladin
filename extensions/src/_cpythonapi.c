/**
 * @file _cpythonapi.c
 * @date 2026/04/15
 * @author Sokyoei
 *
 * 使用 Python C API 编写的模块，可供 Python 直接调用
 */

#define PY_SSIZE_T_CLEAN

#include <stdio.h>

#include <Python.h>

static PyObject* hello_cpython(PyObject* self) {
    printf("Hello CPython!\n");
    Py_RETURN_NONE;
}

static PyObject* dear(PyObject* self) {
    return PyUnicode_FromString("Dear Ahri Nono😍😘");
}

static PyObject* add(PyObject* self, PyObject* args) {
    PyObject *a_obj, *b_obj;
    if (!PyArg_ParseTuple(args, "OO", &a_obj, &b_obj)) {
        return NULL;
    }

    // 检查两个是否都是 Python 整数
    if (PyLong_Check(a_obj) && PyLong_Check(b_obj)) {
        long a_long = PyLong_AsLong(a_obj);
        long b_long = PyLong_AsLong(b_obj);
        if (PyErr_Occurred()) {
            return NULL;
        }
        return PyLong_FromLong(a_long + b_long);
    }

    // 有一个浮点数，浮点数相加
    double a = PyFloat_AsDouble(a_obj);
    double b = PyFloat_AsDouble(b_obj);

    if (PyErr_Occurred()) {
        return NULL;
    }

    return PyFloat_FromDouble(a + b);

    // 原生加法
    // return PyNumber_Add(a_obj, b_obj);
}

static PyMethodDef methods[] = {
    {"hello_cpython", (PyCFunction)hello_cpython,  METH_NOARGS, NULL},
    {         "dear",          (PyCFunction)dear,  METH_NOARGS, NULL},
    {          "add",           (PyCFunction)add, METH_VARARGS, NULL},
    {           NULL,                       NULL,            0, NULL},
};

static struct PyModuleDef module = {
    .m_base = PyModuleDef_HEAD_INIT,
    .m_name = "_cpythonapi",
    .m_doc = NULL,
    .m_size = -1,
    .m_methods = methods,
};

PyMODINIT_FUNC PyInit__cpythonapi(void) {
    return PyModule_Create(&module);
}
