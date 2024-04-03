#include <iostream>
#include <string>

#include <pybind11/numpy.h>
#include <pybind11/pybind11.h>

namespace py = pybind11;
using py::literals::operator""_a;
using py::literals::operator""_s;

namespace Ahri {
    class Person {
    private:
        std::string _name;
        int _age;

    public:
        Person(std::string name, int age) : _name(name), _age(age) {}
        ~Person() {}
        void print_info() { std::cout << "I'm " << _name << ", " << _age << " year old" << std::endl; }
    };

    void hello() {
                std::cout << "hello" << std::endl;
    }

    py::array_t<int> ndarrayReturn(py::array_t<int>& arr) {
        py::buffer_info buffer = arr.request();
        int* ptr = (int*)buffer.ptr;
        std::vector<py::ssize_t> shape = buffer.shape;
        std::vector<py::ssize_t> strides = buffer.strides;
        std::vector<std::vector<std::vector<int>>> mat(shape[0],
            std::vector<std::vector<int>>(shape[1], std::vector<int>(shape[2])));
        for (auto& i : mat) {
            for (auto& j : i) {
                for (auto& k : j) {
                    k = *ptr++;
                    k += 2;
                }
            }
        }
        py::array ret = py::cast(mat);
        return ret;
    }

}  // namespace Ahri

PYBIND11_MODULE(pybind11_example, m) {
    py::class_<Ahri::Person>(m, "Person")
        .def(py::init<std::string, int>())
        .def("print_info", &Ahri::Person::print_info);
    m.def("hello", &Ahri::hello);
}
