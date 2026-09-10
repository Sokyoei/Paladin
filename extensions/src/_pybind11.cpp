#include <iostream>
#include <string>

#include <pybind11/numpy.h>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using py::literals::operator""_a;
using py::literals::operator""_s;

namespace Ahri {
void hello_pybind11() {
    std::cout << "Hello pybind11!" << std::endl;
}

py::object add_pybind11(py::object a, py::object b) {
    // 等价 PyNumber_Add
    return a + b;
}

class Person {
private:
    std::string _name;
    int _age;

public:
    Person(std::string name, int age) : _name(name), _age(age) {}
    void print_info() { std::cout << "I'm " << _name << ", " << _age << " year old" << std::endl; }
};

py::array_t<int> add_ndarray_pybind11(const py::array_t<int>& a, const py::array_t<int>& b) {
    py::buffer_info a_buffer = a.request(true);
    py::buffer_info b_buffer = b.request(true);

    // 维度检查
    if (a_buffer.ndim != b_buffer.ndim) {
        throw std::runtime_error("ndim mismatch");
    }
    // shape 检查
    if (a_buffer.shape != b_buffer.shape) {
        throw std::runtime_error("shape mismatch");
    }

    py::array_t<int> c(a_buffer.shape);
    py::buffer_info c_buffer = c.request();

    int* a_ptr = static_cast<int*>(a_buffer.ptr);
    int* b_ptr = static_cast<int*>(b_buffer.ptr);
    int* c_ptr = static_cast<int*>(c_buffer.ptr);

    for (py::ssize_t i = 0; i < a_buffer.size; ++i) {
        c_ptr[i] = a_ptr[i] + b_ptr[i];
    }
    return c;
}

}  // namespace Ahri

PYBIND11_MODULE(_pybind11, m) {
    m.doc() = "_pybind11 module";

    m.def("hello_pybind11", &Ahri::hello_pybind11);
    m.def("add_pybind11", &Ahri::add_pybind11);
    m.def("add_ndarray_pybind11", &Ahri::add_ndarray_pybind11);

    py::class_<Ahri::Person>(m, "Person")
        .def(py::init<std::string, int>())
        .def("print_info", &Ahri::Person::print_info);
}
