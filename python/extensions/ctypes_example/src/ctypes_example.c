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

typedef struct Ahri {
    int age;
    int* score;
    int score_len;
} Ahri;

AHRI_API void print_Ahri(Ahri* arr, int len) {
    for (int i = 0; i < len; i++) {
        printf("age: %d, ", arr[i].age);
        printf("score_len: %d, ", arr[i].score_len);
        for (int j = 0; j < arr[i].score_len; j++) {
            printf("%d ", arr[i].score[j]);
        }
        printf("\n");
    }
}

AHRI_API void update_Ahri(Ahri* arr, int len) {
    for (int i = 0; i < len; i++) {
        for (int j = 0; j < arr[i].score_len; j++) {
            arr[i].score[j] += 2;
        }
    }
}

int SOKYOEI = 0;

AHRI_API int set_SOKYOEI(int n) {
    SOKYOEI = n;
}

AHRI_API void print_SOKYOEI() {
    printf("SOKYOEI: %d\n", SOKYOEI);
}
