#define PY_SSIZE_T_CLEAN

#include <stdio.h>

#include <Python.h>

PyObject* DearAhri(PyObject* self, PyObject* args) {
    printf("Dear: Ahri");
    return Py_None;
}

PyObject* add(PyObject* self, PyObject* args) {
    int l;
    if (!PyArg_ParseTuple(args, "i", &l)) {
        return NULL;
    }
    // long l = PyLong_AsLong(args);
    l++;
    return PyLong_FromLong(l);
}

static PyMethodDef methods[] = {
    {"DearAhri", DearAhri, METH_VARARGS,   ""},
    {     "add",      add, METH_VARARGS,   ""},
    {      NULL,     NULL,            0, NULL}
};

static PyModuleDef Python_API_example = {
    PyModuleDef_HEAD_INIT, "Python_API_example", "", -1, methods,
};

PyMODINIT_FUNC PyInit_Python_API_example(void) {
    return PyModule_Create(&Python_API_example);
}
