mov ax,0xb800
mov es,ax
; 清屏
mov cx,80*25
clean:
	mov di,cx
	add di,di
	mov byte [es:di],''
	add di,1
	mov byte [es:di],0x0F
	loop clean
; 显示上方白条
; 移除(0,0)的S字符
mov byte [es:0x00],''
mov cx,80*2-1
mov di,0
push cx
headtitle:
	mov di,cx
	mov byte [es:di],0xF0
	; 写入空字符
	add di,di
	mov byte [es:di],''
	;inc cx
	;sub cx,1
	loop headtitle

xor di,di
pop cx
; 显示下方白条
tailtitle:
	mov di,cx
	add di,80*2*24
	mov byte [es:di],0xF0
	; 写入空字符
	mov di,cx
	add di,di
	add di,80*2*24
	mov byte [es:di],''
	loop tailtitle
; 在第一行写入文本
jmp near showHeadText
headText: db 'Wine Runner  Webiste:http://gitee.com/gfdgd-xi/deep-wine-runner'
showHeadText:
; 虽然可以简单粗暴的用 movsw，但是会出现问题
	mov cx,showHeadText-headText
	mov ax,0x7c0
	mov ds,ax ; 定位到汇编程序所在的内存地址
	showHeadTextLoop:
		mov dx,cx
		mov di,cx
		add di,di
		mov si,headText
		sub dx,1
		add si,dx
;		inc si
;		mov al,1000
		mov al,[ds:si]
		mov byte [es:di],al
		loop showHeadTextLoop
jmp near showTailText
tailText: db '2020~Now gfdgd xi'
showTailText:
	mov cx,showTailText-tailText
	mov ax,0x7c0
	mov ds,ax
	showTailTextLoop:
		mov dx,cx
		mov di,cx
		add di,di
		add di,80*2*24
		mov si,tailText
		sub dx,1
		add si,dx
		mov al,[ds:si]
		mov byte [es:di],al
		loop showTailTextLoop

; 显示中部提示文本
jmp near showCenterText
centerTextScreenSize:
	; 第一位是行数
	; 第二位是单行偏移量
	db 1, -1
centerText: 
	db 'Mode: Real Mode Demo', 0x0A
	db 'Bit: 16', 0x0A
	db 'Virtual Machine: qemu-system-i386'
	db  0x03  ; 结束符
showCenterText:
	centerTextLong equ showCenterText-centerText
	mov cx,centerTextLong
	xor ax,ax
	loopShowCenterText:
		jmp near addScreenLineFinish
		addScreenLine:
			; 如果检测到换行符
			mov dx, [centerTextScreenSize]
			add dx,1
			mov [centerTextScreenSize], dx
			dec cx
			mov al,-1
			mov [centerTextScreenSize+1],al
			; 行数+1，偏移量设为 -1（从头开始）
			;ret
		addScreenLineFinish:
		; 偏移量 + 1
		mov al,[centerTextScreenSize+1]
		add al,1
		mov [centerTextScreenSize+1],al
		mov di,centerText
		add di,centerTextLong
		sub di,cx
		mov bl,[di]

		; 判断是不是结束符
		cmp bl,0x03
		je showCenterTextEnd
		
		; 判断是不是换行符
		cmp bl,0x0A
		je addScreenLine ; 换行符检测

		xor ah,ah ; 清空高位
		add al,al
		mov di,ax
		
		; 计算显示位置
		xor dx,dx
		mov dl,[centerTextScreenSize]
		mov ax,80
		mul dx
		mov dx,2
		mul dx
		add ax,2
		add di,ax

		; 显示
		mov byte [es:di], bl
		loop loopShowCenterText

showCenterTextEnd:

;mov ax,[cs:0x100]
;mov dx,[cs:0x102]
;	mov bx,16
;	div bx
;	mov ds,ax
;	mov es,ax
;xor di,di
;mov si,1
;xor ds,ds
;mov bx,512
;xor bx,bx
;call read_hard_disk_0


get_data:
	mov di,80*2*25-2

	; 读取秒
	mov al,0x00
	call read_time
	mov byte [es:di-4],':'
	mov byte [es:di-2],ah
	mov byte [es:di],al
	; 读取分钟
	mov al,0x02
	call read_time
	mov byte [es:di-10],':'
	mov byte [es:di-8],ah
	mov byte [es:di-6],al
	; 读取小时
	mov al,0x04
	call read_time
	mov byte [es:di-14],ah
	mov byte [es:di-12],al
	; 读取日
	mov al,0x07
	call read_time
	mov byte [es:di-22],'.'
	mov byte [es:di-20],ah
	mov byte [es:di-18],al
	; 读取月
	mov al,0x08
	call read_time
	mov byte [es:di-28],'.'
	mov byte [es:di-26],ah
	mov byte [es:di-24],al
	; 读取年
	mov al,0x09
	call read_time
	mov byte [es:di-32],ah
	mov byte [es:di-30],al


hlt  ; 使用停机指令降低 CPU 使用率
jmp near get_data


read_time:
	out 0x70,al
	in al,0x71
	call bcd_to_ascii
	ret

; 用于编码转换：BCD=》ASCII
; 输入：AL=bcd码
; 输出：AX=ascii
bcd_to_ascii:
	mov ah,al
	and al,0x0f
	add al,0x30

	shr ah,4
	and ah,0x0f
	add ah,0x30
	ret

;poweroff:
	; 关机
;	mov ax,5307H  ; 高级电源管理功能，设置电源状态
;	mov bx,0001H  ; 设备ID，1：所有设备
;	mov cx,0003H  ; 状态，3：表示关机
;	int 15h



end:
	times 510-($-$$) db 0
	db 0x55,0xaa

; 后面部分暂时废弃


read_hard_disk_0:  ; 从硬盘读取一个逻辑扇区
		; 输入：DI:SI=起始逻辑扇区号
		; DS:BX=目标缓冲区地址
	push ax
	push bx
	push cx
	push dx

	mov dx,0x1f2
	mov al,1
	out dx,al ; 读取的扇区数

	inc dx ; 0x1f3
	mov ax,si
	out dx,al ; LBA地址7~0

	inc dx ; 0x1f4
	mov al,ah
	out dx,al ; LBA地址15~8

	inc dx ; 0x1f5
	mov ax,di
	out dx,al ; LBA地址23~16

	inc dx ; 0x1f6
	mov al,0xe0 ; LBA28模式，主盘
	or al,ah ; LBA地址27~24
	out dx,al

	inc dx ; 0x1f7
	mov al,0x20 ; 读命令
	out dx,al

	.waits:
		in al,dx  ; 此时 dx 为 0x1f7，此时为命令端口也是状态窗口
		and al,0x88
		cmp al,0x08
		jnz .waits
		; 内部操作期间，会将 0x1f7 端口第 7 位设置为“1”，准备就绪后会将此位清零，并将第 3 位设为 1

		mov cx,256 ; 总计要读取的/字/数
		mov dx,0x1f0
	
	.readw:
		in ax,dx
		mov [bx],ax
		add bx,2
		loop .readw

		pop dx
		pop cx
		pop bx
		pop ax


