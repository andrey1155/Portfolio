#define _CRT_SECURE_NO_WARNINGS
#include <stdint.h> // uint16_t
#include <stdio.h>  // FILE
#include <signal.h> // SIGINT
/* windows only */
#include <Windows.h>
#include <conio.h>  // _kbhit
#include <assert.h>
#include <math.h>
#include <cmath>
#include <locale.h>
#include <ctime>
#define ROUND_2_INT(f) ((int)(f >= 0.0 ? (f + 0.5) : (f - 0.5)))
#define R_COUNT 14

HANDLE hStdin = INVALID_HANDLE_VALUE;

uint16_t check_key() {
    return WaitForSingleObject(hStdin, 1000) == WAIT_OBJECT_0 && _kbhit();
}

DWORD fdwMode, fdwOldMode;

void disable_input_buffering()
{
    hStdin = GetStdHandle(STD_INPUT_HANDLE);
    GetConsoleMode(hStdin, &fdwOldMode); /* save old mode */
    fdwMode = fdwOldMode
        ^ ENABLE_ECHO_INPUT  /* no input echo */
        ^ ENABLE_LINE_INPUT; /* return when one or
                                more characters are available */
    SetConsoleMode(hStdin, fdwMode); /* set new mode */
    FlushConsoleInputBuffer(hStdin); /* clear buffer */
}

void restore_input_buffering()
{
    SetConsoleMode(hStdin, fdwOldMode);
}

void handle_interrupt(int signal)
{
    restore_input_buffering();
    printf("\n");
    exit(-2);
}

//flags
enum
{
    MR_KBSR = 127, /* keyboard status */
    MR_KBDR = 126  /* keyboard data */
};

enum
{
    FL_POS = 1 << 0,	// p
    FL_ZRO = 1 << 1,	// z
    FL_NEG = 1 << 2		// n
};


//registres
enum {
    R0 = 0,
    R1,
    R2,
    R3,
    R4,
    BP,
    SP,
    BUFF,
    PC,
    COND,
    RSUB,
};


//major opcodes
enum {
    LD = 0,
    ST,
    MOV,

    AND_OR,
    NOT_XOR,

    MATH_AND_SHIFT,
    DIV_UDIV,
    FMATH,

    BR,
    BR_JMP,
    JSR,

    TRAP,

    FILE_IO,

    VMBOOLEAN,

    OR = 14
};

//float opcodees
enum {
    fadd,
    fsub,
    fmul,
    fdiv,
    exp_,
    sqrt_,
    ln_
};

//traps
enum
{
    CHAR_OUT = 0,
    INT_OUT = 1,
    UINT_OUT = 2,
    FLOAT_OUT = 3,

    TRAP_GETC = 4,

    TRAP_PUSH = 5,
    TRAP_POP = 6,

    TRAP_CLS = 7,
    TRAP_HALT = 8,

    TRAP_RET = 9,

    TRAP_INC,
    TRAP_DEC,
    TRAP_INV
};

uint16_t memory[UINT16_MAX];
uint16_t reg[R_COUNT];
uint8_t operating = 1;

#pragma region Float16Tools

struct float16 {
    int8_t m;
    int8_t e;
};

inline int8_t boost_order(double m, int* exp) {
    int8_t mant = 0;

    while (abs(m) < 63 && m != 0) {
        m *= 2;
        *exp -= 1;
    }
    mant = ROUND_2_INT(m);
    return mant;
}

inline float getFloat(float16 f16) {
    return f16.m * pow(2, f16.e);
}

inline float16 getF16(float f) {
    int exp = 0;
    float m = frexp(f, &exp);

    float16 ret;
    ret.m = boost_order(m, &exp);
    ret.e = exp;
    return ret;
}

inline uint16_t float16_to_int(float16 f) {
    uint16_t ret;
    ret = f.m << 8;
    ret |= f.e & 0xFF;
    return ret;
}

inline float16 int_to_float16(uint16_t f) {
    float16 ret;
    ret.e = f & 0xFF;
    ret.m = (f & 0xFF00) >> 8;
    return ret;
}

inline uint16_t float_to_uint16_t(float f) {
    float16 t = getF16(f);
    return float16_to_int(t);
}

inline float uint16_t_to_float(uint16_t u) {
    float16 t = int_to_float16(u);
    return getFloat(t);
}

#pragma endregion

uint16_t sign_extend(uint16_t x, int bit_count)
{
    if ((x >> (bit_count - 1)) & 1) {
        x |= (0xFFFF << bit_count);
    }
    return x;
}

inline void update_flags(uint16_t r) {
    if (reg[r] == 0)
        reg[COND] = FL_ZRO;
    else if (reg[r] >> 15) //gets first bit, representing sign
        reg[COND] = FL_NEG;
    else
        reg[COND] = FL_POS;
}

#pragma region Memory controll

inline void mem_write(uint16_t adress, uint16_t val) {
    memory[adress] = val;
}

inline uint16_t mem_read(uint16_t adress) {
    if (adress == MR_KBSR) {
        if (check_key()) {
            memory[MR_KBSR] = (1 << 15);
            memory[MR_KBDR] = getchar();
        }
        else {
            memory[MR_KBSR] = 0;
        }
    }
    return memory[adress];
}

#pragma endregion

#pragma region MemoryINSTR

inline void f_LD(uint16_t instr) {
    uint16_t second_opcode = (instr >> 10) & 0x3;

    uint16_t operand_2 = instr & 127;           //adress / reg adress /  offset
    uint16_t operand_1 = (instr >> 7) & 0x7;    //reg or base

    switch (second_opcode)
    {
    case 0:
    {
        reg[operand_1] = mem_read(operand_2);
        update_flags(operand_1);
        break;
    }
    case 1:
    {
        reg[operand_1] = mem_read(reg[operand_2 & 0x7]);
        update_flags(operand_1);
        break;
    }
    case 2:
    {
        reg[BUFF] = mem_read(reg[operand_1] + operand_2);
        update_flags(BUFF);
        break;
    }
    case 3:
    {
        reg[BUFF] = mem_read(mem_read(reg[operand_1] + operand_2));
        update_flags(BUFF);
        break;
    }
    default:
        break;
    }
}

inline void f_STR(uint16_t instr) {
    uint16_t second_opcode = (instr >> 10) & 0x3;

    uint16_t operand_2 = instr & 127;           //adress / reg adress /  offset
    uint16_t operand_1 = (instr >> 7) & 0x7;    //reg or base

    switch (second_opcode)
    {
    case 0:
    {
        mem_write(operand_2, reg[operand_1]);
        break;
    }
    case 1:
    {
        mem_write(reg[operand_2 & 0x7], reg[operand_1]);
        break;
    }
    case 2:
    {
        mem_write(reg[operand_1 & 0x7] + operand_2, reg[BUFF]);
        break;
    }
    case 3:
    {
        mem_write(mem_read(reg[operand_1 & 0x7] + operand_2), reg[BUFF]);
        break;
    }
    default:
        break;
    }
}

inline void f_MOV(uint16_t instr) {
    if (instr & (1 << 11)) {
        uint16_t rd = (instr >> 4) & 0xF;
        uint16_t value = instr & 0xF;

        reg[rd] = reg[value];
        update_flags(rd);
    }
    else {
        uint16_t rd = (instr >> 8) & 7;
        uint16_t value = instr & 0xFF;

        reg[rd] = value;
        update_flags(rd);
    }
}

#pragma endregion 

#pragma region MATH
inline void f_AND_OR(uint16_t instr) {
    uint16_t rd = (instr >> 7) & 0x7;

    uint8_t secondOP = (instr >> 11) & 0x1;
    uint8_t imm_flag = (instr >> 10) & 0x1;

    uint8_t r2 = instr & 0x7;
    uint8_t imm7 = instr & 0x7F;

    if (secondOP == 0) {

        if (imm_flag) {
            reg[rd] = reg[rd] & imm7;
        }
        else {
            reg[rd] = reg[rd] & reg[r2];
        }

    }
    else {

        if (imm_flag) {
            reg[rd] = reg[rd] | imm7;
        }
        else {
            reg[rd] = reg[rd] | reg[r2];
        }

    }
    update_flags(rd);
}

inline void f_NOT_XOR(uint16_t instr) {
    uint16_t rd = (instr >> 7) & 0x7;

    uint8_t secondOP = (instr >> 11) & 0x1;
    uint8_t imm_flag = (instr >> 10) & 0x1;

    if (secondOP == 0) {

        reg[rd] = !reg[rd];
        update_flags(rd);
       
    }
    else {

        if (imm_flag) {
            uint8_t imm7 = instr & 0x7F;

            reg[rd] = reg[rd] ^ imm7;
            update_flags(rd);
        }
        else {
            uint8_t r2 = instr & 0x7;

            reg[rd] = reg[rd] ^ reg[r2];
            update_flags(rd);
        }

    }
}

inline void f_ADD_SUB_MUL_and_SHIFT(uint16_t instr) {
    uint16_t rd = (instr >> 6) & 0x7;

    uint8_t secondOP = (instr >> 10) & 0x3;
    uint8_t imm_flag = (instr >> 9) & 0x1;

    uint8_t r2 = instr & 0x7;
    uint8_t imm6 = instr & 0x3F;


    switch (secondOP) {
    case 0: 
        if (imm_flag) {
            reg[rd] = reg[rd] + imm6;
        }
        else {
            reg[rd] = reg[rd] + reg[r2];
        }
        break;
    case 1:
        if (imm_flag) {
            reg[rd] = reg[rd] - imm6;
        }
        else {
            reg[rd] = reg[rd] - reg[r2];
        }
        break;
    case 2:
        if (imm_flag) {
            reg[rd] = reg[rd] * imm6;
        }
        else {
            reg[rd] = reg[rd] * reg[r2];
        }
        break;
    case 3:
        if (imm_flag) {
            reg[rd] = reg[rd] << imm6;
        }
        else {
            reg[rd] = reg[rd] >> imm6;
        }
        break;

    }

    update_flags(rd);
}

inline void f_DIV_UDIV(uint16_t instr) {
    uint16_t rd = (instr >> 7) & 0x7;

    uint8_t secondOP = (instr >> 11) & 0x1;
    uint8_t imm_flag = (instr >> 10) & 0x1;

    uint8_t r2 = instr & 0x7;
    uint8_t imm7 = instr & 0x7F;

    if (secondOP == 0) {

        if (imm_flag) {
            reg[rd] = reg[rd] / imm7;
        }
        else {
            reg[rd] = reg[rd] / reg[r2];
        }

    }
    else {

        if (imm_flag) {
            reg[rd] = (uint16_t)reg[rd] / (uint16_t)imm7;
        }
        else {
            reg[rd] = (uint16_t)reg[rd] / (uint16_t)reg[r2];
        }

    }
    update_flags(rd);
}

inline void f_FLOAT_OPS(uint16_t instr) {

    uint16_t operand_1 = (instr >> 3) & 0x7;
    uint8_t secondOP = (instr >> 6) & 0x7;
    uint8_t operand_2 = instr & 0x7;

    float n1, res;

    switch (secondOP) {
    case fadd:
        res = uint16_t_to_float(reg[operand_2]) + uint16_t_to_float(reg[operand_1]);
        reg[operand_1] = float_to_uint16_t(res);
        break;
    case fsub:
        res = uint16_t_to_float(reg[operand_1]) - uint16_t_to_float(reg[operand_2]);
        reg[operand_1] = float_to_uint16_t(res);
        break;
    case fmul:
        res = uint16_t_to_float(reg[operand_2]) * uint16_t_to_float(reg[operand_1]);
        reg[operand_1] = float_to_uint16_t(res);
        break;
    case fdiv:
        res = uint16_t_to_float(reg[operand_1]) / uint16_t_to_float(reg[operand_2]);
        reg[operand_1] = float_to_uint16_t(res);
        break;


    case exp_:
        n1 = uint16_t_to_float(reg[operand_1]);
        res = exp(n1);

        reg[operand_1] = float_to_uint16_t(res);
        break;
    case sqrt_:
        n1 = uint16_t_to_float(reg[operand_1]);
        res = sqrt(n1);

        reg[operand_1] = float_to_uint16_t(res);
        break;
    case ln_:
        n1 = uint16_t_to_float(reg[operand_1]);
        res = log(n1);

        reg[operand_1] = float_to_uint16_t(res);
        break;

    }
   
    update_flags(operand_1);
}

#pragma endregion 

#pragma region ControllFLOW
inline void f_BRANCH(uint16_t instr) {
    uint16_t cond = (instr >> 9) & 0x7;
    uint16_t dir = (instr >> 8) & 1;
    uint16_t pc_offset = instr & 0xFF;


    if (cond & reg[COND]) {
        if (dir)
            reg[PC] += pc_offset - 1;
        else
            reg[PC] -= (pc_offset + 1);
    }
}

inline void f_BRANCH_JSR(uint16_t instr) {
    uint16_t cond = (instr >> 9) & 0x7;
    uint16_t dir = (instr >> 8) & 1;
    uint16_t base_offset = instr & 0x3F;
    uint16_t base = (instr >> 6) & 0x7;
     
    if (cond & reg[COND]) {
        if (dir)
            reg[PC] += reg[base] + base_offset - 1;
        else
            reg[PC] -= reg[base] + (base_offset + 1);
    }
}

inline void f_JSR(uint16_t instr) {
    reg[RSUB] = reg[PC];

    uint16_t pc_offset = instr & 0x1FF;
    uint16_t base_r = (instr >> 9) & 0x7;

    reg[PC] = reg[base_r] + pc_offset;
}
#pragma endregion

inline void f_TRAP(uint16_t instr) {

    uint16_t r = (instr >> 8) & 0xF;
    uint16_t trap = instr & 0xFF;
    switch (trap)
    {
    case TRAP_GETC:
        /* TRAP GETC */
        /* read a single ASCII char */
        reg[BUFF] = (uint16_t)_getch();

        break;
    case CHAR_OUT:
        /* TRAP OUT */
        putc((char)reg[r], stdout);
        fflush(stdout);

        break;

    case UINT_OUT:
    {
        printf("%u", reg[r]);
        break;
    }

    case INT_OUT:
    {
        printf("%i", (int16_t)reg[r]);
        break;
    }

    case FLOAT_OUT:
    {
        float out = uint16_t_to_float(reg[r]);
        printf("%f", out);

        break;
    }

    case TRAP_HALT:
        /* TRAP HALT */
        fflush(stdout);
        operating = 0;

        break;

    case TRAP_PUSH:
    {
        mem_write(reg[SP], reg[r]);
        reg[SP]++;
        break;
    }

    case TRAP_POP:
        reg[SP]--;
        reg[r] = mem_read(reg[SP]);
        break;

    case TRAP_CLS:
        system("cls");
        break;

    case TRAP_RET:
        reg[PC] = reg[RSUB];
        break;

    case TRAP_INC:
        reg[r]++;
        break;

    case TRAP_DEC:
        reg[r]++;
        break;

    case TRAP_INV:
        reg[r]*=-1;
        break;
    }
}



inline void f_BOOLEAN(uint16_t instr) {
    uint16_t second_opcode = (instr >> 10) & 0x3;
    uint8_t imm_flag = (instr >> 9) & 0x1;

    uint16_t operand_2 = instr & 0x3F;         
    uint16_t operand_1 = (instr >> 6) & 0x7;    


    switch (second_opcode)
    {
    case 0:
    {
        if(!imm_flag)
            reg[COND] = reg[operand_1] - reg[operand_2];
        else
            reg[COND] = reg[operand_1] - operand_2;
        update_flags(COND);
        break;
    }
    case 1:
    {
        //WTF
        if (!imm_flag)
            if(reg[operand_1] | reg[operand_2])
                reg[COND] = FL_POS;
            else
                reg[COND] = FL_NEG|FL_ZRO;
            
        else
            if (reg[operand_1] | operand_2)
                reg[COND] = FL_POS;
            else
                reg[COND] = FL_NEG | FL_ZRO;
        break;
    }
    case 2:
    {
        if (reg[operand_1] == 0)
            reg[operand_1] = 1;
        else
            reg[operand_1] = 0;
        break;
    }
    default:
        break;
    }
}

inline void f_OR(uint16_t instr) {

    if (instr == 0xFFFF)return;

    uint16_t data = instr & 0xFF;
    uint16_t r = (instr >> 8) & 0x7;


    reg[r] = reg[r] << 8;
    reg[r] |= data;
    update_flags(r);
}

#pragma region File IO

void read_image_file(FILE* file) {
    size_t read = fread(memory, sizeof(uint16_t), UINT16_MAX, file);
}

int read_image(const char* image_path) {
    FILE* file = fopen(image_path, "rb");
    if (!file)return 0;
    read_image_file(file);
    fclose(file);
    return 1;
}

#pragma endregion


int main(int argc, const char* argv[])
{
    signal(SIGINT, handle_interrupt);
    disable_input_buffering();
    setlocale(LC_ALL, "Rus");

    if (argc == 1) {
        argc = 2;
        argv[1] = "test.obj";
    }

    bool pause_flag = true;

    if (argc == 3)
        if (argv[2] == "false")
            pause_flag = false;

    if (argc == 1)
    {
        // show usage string 
        printf("Error: unvalid input \n");
        exit(2);
    }

    if (!read_image(argv[1]))
    {
        printf("failed to load image: %s\n", argv[1]);
        exit(1);
    }



    reg[COND] = 1;
    reg[PC] = memory[0];
    reg[BP] = memory[1];
    reg[SP] = memory[1];

    while (operating) {

        uint16_t instr = memory[reg[PC]++];
        uint16_t op = instr >> 12;

        switch (op)
        {
        case MOV:
            f_MOV(instr);
            break;
        case ST:
            f_STR(instr);
            break;
        case LD:
            f_LD(instr);
            break;


        case AND_OR:
            f_AND_OR(instr);
            break;
        case NOT_XOR:
            f_NOT_XOR(instr);
            break;


        case MATH_AND_SHIFT:
            f_ADD_SUB_MUL_and_SHIFT(instr);
            break;
        case DIV_UDIV:
            f_DIV_UDIV(instr);
            break;
        case FMATH:
            f_FLOAT_OPS(instr);
            break;

        case BR:
            f_BRANCH(instr);
            break;
        case BR_JMP:
            f_BRANCH_JSR(instr);
            break;
        case JSR:
            f_JSR(instr);
            break;

        case TRAP:
            f_TRAP(instr);
            break;

        case VMBOOLEAN:
            f_BOOLEAN(instr);
            break;

        case OR:
            f_OR(instr);
            break;
            
        default:
            assert("error");
            break;
        }

    }

    restore_input_buffering();
    printf("\n");
    if (pause_flag)
        system("pause");
}