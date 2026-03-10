; Hola Mundo;
; creado por: David
; fecha: 26/02/2026
; compilar con: nasm -f elf hola01.asm
; vincular con: ld -m elf_i386 hola01.o -o holamundo01

SECTION .data
	msg	db	'Hola mundo!',0Ah	; cadena msg = 'Hola mundo!'

SECTION .text
	global _start

_start:
        mov     eax, msg        ; eax = direccion de msg
        call 	srtLen

	; Despliegue de cadena en pantalla
	        mov     edx, eax                ; edx = 12 (Numero de caracteres)
	        mov     ecx, msg                ; ecx = msg (direccion de cadena)
	        mov     ebx, 1                  ; escribe al STDOUT_file
	        mov     eax, 4                  ; invocar a SYS_WRITE
	        int     80h

	   ; Salida al Sistema
	        mov     ebx, 0                  ; return 0
	        mov     eax, 1                  ; invoca a SYS_EXIT
	        int     80h

; --------------------- CALCULO DE Tamaño de Cadena ------------------------

strLen:
	push 	ebx		; guardar en pila el contendio de ebx
        mov     ebx, eax       ; ebx = direccion de msg
 

sigChar:
        cmp     byte [eax], 0   ; si [eax] == NULL
        jz      finConteo
        inc     eax
        jmp     sigChar

finConteo:

        sub     eax, ebx        ; eax -= ebx
	pop	ebx
	red
