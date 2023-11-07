#include <iostream>
#include <string>

#include <pybind11/pybind11.h>

namespace py = pybind11;

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
}  // namespace Ahri

PYBIND11_MODULE(AhriCXX, m) {
    py::class_<Ahri::Person>(m, "Person")
        .def(py::init<std::string, int>())
        .def("print_info", &Ahri::Person::print_info);
    m.def("hello", &Ahri::hello);
}
