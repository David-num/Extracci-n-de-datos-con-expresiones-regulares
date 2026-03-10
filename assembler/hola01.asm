;Hola mundo!
;creado por: David
;fecha: 24 de febrero 2026
;compilar: nasm -f elf hola01.asm
;vincular con: ld -m elf_i386 hola01.o -o holamundo01

SECTION .data
	msg	db	'Hola mundo!',0Ah	; cadena msg = 'Hola mundo!'

SECTION .text
global _start

_start:
	; Despliege de cade en pantalla
	mov	edx,12		;edx = 12 (numero de caracteres)
	mov	ecx,msg		;ecx = msg (direccion de cadena)
	mov 	ebx,1		;escrive al STDOUT_file
	mov 	eax,4		;invocar a SYS_WRITE
	int	80h

	; Salida al sistema
	mov	ebx,0		;return 0
	mov 	eax,1		;invoca a SYS_EXIT
	int 	80h
