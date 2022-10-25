.def

@define null 0
@define bel 7
@define bsp 8
@define tab 9
@define endl 10
@define vtab 11
@define cret 13

.data

.code

@label print_string

ld buff, r4

@label loop_ps
putc buff
inc r4
ld buff, r4

cmp buff, 0
brne loop_ps

ret

@label init_string

getc buff

st buff, r4
inc r4
cmp buff, cret 

brne init_string

mov buff, 0
st buff, r4
ret

@macro putcd symbol
mov buff, symbol
putc buff
@endmacro



