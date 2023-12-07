// gcc (-g) -shared -fPIC .\AhriC.c -o .\AhriC.dll
//
// cl /c Ahri.c
// link /dll Ahri.obj

#include <stdio.h>
#include <string.h>

#ifdef _MSC_VER
#define AHRI_API __declspec(dllexport)
#elif defined(__GNUC__)
#define AHRI_API __attribute__((visibility("default")))
#endif

typedef int (*int_x3_ptr)[3];

// array
AHRI_API int_x3_ptr array_add(int_x3_ptr arr) {
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            arr[i][j]++;
        }
    }
    return arr;
}

// struct
typedef struct Student {
    int age;
    char* name;
} Student;

typedef Student (*Student_3)[3];

AHRI_API Student* student_add(Student* stus) {
    for (int i = 0; i < 3; i++) {
        stus[i].age += 1;
    }
    return stus;
}
