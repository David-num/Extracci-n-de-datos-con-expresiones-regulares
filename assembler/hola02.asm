;Hola mundo! version 3
;creado por: david
;fecha: 24 de febrero de 2026
;compilar: nasm -f elf hola02.asm
;vincular con: ld -m elf_i386 hola02.o -o holamundo02

SECTION .data
	msg db	"Hola mundo version 3!",0Ah	;cadena msg = "Hola mundo!"

SECTION .text
global _start

_start:
	mov eax,msg		; eax = direccion de msg
	call strLen

        ; Despliegue de cadena en pantalla
        mov     edx, 12                 ; edx = 12 (Numero de caracteres)
        mov     ecx, msg                ; ecx = msg (direccion de cadena)
        mov     ebx, 1                  ; escribe al STDOUT_file
        mov     eax, 4                  ; invocar a SYS_WRITE
        int     80h

        ; Salida al Sistema
        mov     ebx, 0                  ; return 0
        mov     eax, 1                  ; invoca a SYS_EXIT
        int     80h

;----------------------------------------Calculo de tamaño de cadena---------------------------------------

strLen:
	push 	ebx		;guardar en pila el contenido de ebx
	mov	ebx,eax 	; ebx = direccion de msg

sigChar:
        cmp     byte [eax], 0   ; si [eax] == NULL
        jz      finConteo
        inc     eax
        jmp     sigChar

finConteo:

        sub     eax, ebx
	pop 	ebx
	ret
