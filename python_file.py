import serial
import tkinter as t 

def plot():
    global can,sig,sig_
    can.delete(sig)

    if len(sig_)>=4:
        sig=can.create_line(sig_,fill="cyan")

    root.after(5,plot)


def run():
    global sig_,sig_1,count,amp,val,state
    if state==1:
        amp=float(amp*540/1023)

        if not count>810:
            if  count>=5:
                sig_.append([count,543-amp])
                sig_1.append(543-amp)
        else:
            ss=[]
            sig_1.pop(0)
            sig_1.append(543-amp)

            c=5
            for a in sig_1:
                ss.append(c)
                ss.append(a)
                c+=1
            sig_=ss


        amp=round(float(amp*5/540),3)
        count+=1
    else:
        amp=""

    can.delete(val)
    val=can.create_text(820-3,595-37,text=amp,anchor="e",fill="#000000",font=("FreeMono","15","bold"))

    root.after(1,run)



def try_connect():
    global ser,com

    import serial.tools.list_ports
    ports = serial.tools.list_ports.comports()

    for port, desc, hwid in sorted(ports):
            if desc.upper().find("USB-SERIAL")!=-1:
                com=port.upper()
    try:
        ser = serial.Serial(port=str(com), baudrate=9600, bytesize=8, parity='N',stopbits=1, timeout=1 )
    except:
        pass    




def getval():
    global ser,amp,state,count,sig_,sig_1,mess

    try:
        msg = str(ser.readline())
        if not msg=="b''":
            msg=msg.split("b'")[1].split("\\")[0]
            amp=int(msg)
            mess.place_forget()
            state=1
        else:
            state=0
            count=5
            sig_1=[]
            sig_=[]
            sig_1=[]
            try_connect()
            mess.place(in_=root,x=260,y=211.5)

    except:
        state=0
        count=5
        sig_=[]
        sig_=[]
        sig_1=[]
        mess.place(in_=root,x=260,y=211.5)        
        try_connect()

    root.after(1,getval)



amp=0
root=t.Tk()
root.geometry("820x568+0+0")
root.title("oscilloscope")
root.resizable(0,0)
root["bg"]="#d1ffd5"

can=t.Canvas(bg="#f3f3f3",width=820,height=610-37,relief="flat",highlightthickness=0,border=0)
can.place(in_=root,x=0,y=0)

can.create_rectangle(1,1,818,545,fill="#000000",outline="#f3f3f3")

mess=t.Canvas(bg="#000000",width=300,height=150,relief="flat",highlightthickness=0,border=0)

mess.create_oval(0,0,10,10,fill="#f3f3f3",outline="#f3f3f3")
mess.create_oval(0,139,10,149,fill="#f3f3f3",outline="#f3f3f3")
mess.create_oval(289,0,299,10,fill="#f3f3f3",outline="#f3f3f3")
mess.create_oval(289,139,299,149,fill="#f3f3f3",outline="#f3f3f3")
mess.create_polygon(0,5, 0,150-6, 5,150, 299-5,150, 299,150-6, 299,5, 299-5,0, 5,0,fill="#f3f3f3",outline="#f3f3f3" )
mess.create_polygon(150,6, 120,52, 180,52,fill="yellow",outline="#131313",width=2 )
mess.create_oval(150-4,10+7, 150+4,18+7, fill="#131313",outline="#131313",)
mess.create_oval(150-3,10+7+15, 150+3,16+7+15, fill="#131313",outline="#131313",)
mess.create_oval(150-3.5,10+7+25, 150+3.5,17+7+25, fill="#131313",outline="#131313",)
mess.create_polygon(146,21, 147,35, 153,35, 154,21,  fill="#131313",outline="#131313")
mess.create_text(150,90,text="Plug in the hardware.",font=("FreeMono","13"))


val=()
sig=()
sig_=[]
sig_1=[]
ser=0

count=0
state=1

try_connect()
getval()
run()
plot()

root.mainloop()
