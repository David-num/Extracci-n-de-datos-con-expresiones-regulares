; Bloque de funciones de entrada-salida estandar de 32 bit;
; Creado por: David
; fecha: 26 de febrero de 2026

;----------------------Calculo de Tamaño de Cadena ----------------------------

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
	ret

;--------------- printStr(eax = cadena)--------------
printStr:
	push 	edx			;edx a pila
	push	ecx			;ecx a pila
	push 	ebx			;ebx a pila
	push	eax			;eax a pila (es la direccion de cadena)

	call	strLen			; llamada a calculo de longitud de cadena
					; la longitud se devueve en eax

	mov     edx, eax                ; edx = 12 (Numero de caracteres)
        pop 	ecx	                ; ecx = msg (direccion de cadena)
        mov     ebx, 1                  ; escribe al STDOUT_file
        mov     eax, 4                  ; invocar a SYS_WRITE
        int     80h

	pop 	ebx 			; extraer pila en ebx
	pop 	ecx			; extraer pila en ecx
	pop 	edx			; extraer pila en edx
	ret

;---------------printStrLn(eax = cadena)
printStrLn:
	call	printStr		; imprecion de cadena
	push	eax			; resguardar eax
	mov	eax, 0Ah		; eax = 0Ah (ENTER)
	push	eax			; colar el valor de eax en pila
	mov	eax, esp		; eax = Puntero de pila $$
	call	printStr
	pop	eax
	pop	eax
	ret

;---------------Salida al Sistema----------------

quit:
        mov     ebx, 0          ;return 0
        mov     eax, 1          ; invoca SYS_EXIT
        int     80h
