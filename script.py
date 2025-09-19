import tkinter as tk
import colorsys
hue = 0

step = -1
blink_on = True
password_visible = True
is_animating = False

def round_rectangle(canvas, x1, y1, x2, y2, radius=20, **kwargs):
    points = [
        x1 + radius, y1,
        x2 - radius, y1,
        x2, y1,
        x2, y1 + radius,
        x2, y2 - radius,
        x2, y2,
        x2 - radius, y2,
        x1 + radius, y2,
        x1, y2,
        x1, y2 - radius,
        x1, y1 + radius,
        x1, y1
    ]
    return canvas.create_polygon(points, smooth=True, **kwargs)

common_patterns = ["1234","qwerty","11111","123","abc123","0000","password","7777","999","qwertyuiop","444","333","8888","6666","789","4567","789"]
def check_pattern(paswd):
    for pattern in common_patterns:
        if pattern in paswd.lower():
            return True
    return False

def type_text(widget, text, color="lime", font=("Courier New", 14, "bold"), speed=50):
    global is_animating
    is_animating = True
    widget.config(text="", fg=color, font=font)

    def animate(i=0):
        global is_animating
        if i <= len(text):
            widget.config(text=text[:i])
            widget.after(speed, animate, i + 1)
        else:
            is_animating = False

    animate()

def rgb_animation(widget, text=None, font=("Segoe UI", 24, "bold"), speed=50):
    global hue

    if text is not None:
        widget.config(text=text)
    if font is not None:
        widget.config(font=font)

    r, g, b = colorsys.hsv_to_rgb(hue, 1, 1)
    r, g, b = int(r * 255), int(g * 255), int(b * 255)
    widget.config(fg=f'#{r:02x}{g:02x}{b:02x}')
    hue = (hue + 0.01) % 1
    widget.after(speed, lambda: rgb_animation(widget, None, font, speed))

def show_watermark(show=True):
    if show:
        watermark.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-35)
        watermark2.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-10)
    else:
        watermark.place_forget()
        watermark2.place_forget()

def toggle_password():
    global password_visible
    if password_visible:
        entry_pass.config(show="*")
        btn_toggle_canvas.itemconfig(btn_toggle_text, text="Show")
    else:
        entry_pass.config(show="")
        btn_toggle_canvas.itemconfig(btn_toggle_text, text="Hide")
    password_visible = not password_visible

def create_account():
    global step, is_animating
    if is_animating:
        return

    uname = entry_name.get().strip()
    paswd = entry_pass.get()
    digits = [int(c) for c in paswd if c.isdigit()]
    total = sum(digits)

    if step == -1:
        if len(paswd) < 8:
            type_text(label_message, "Password must contain at least 8 characters", "red", speed=15)
            return
        elif not any(char.isupper() for char in paswd):
            type_text(label_message, "Password must contain an uppercase letter", "red", speed=15)
            return
        elif not any(char.islower() for char in paswd):
            type_text(label_message, "Password must contain a lowercase letter", "red", speed=15)
            return
        elif check_pattern(paswd):
            type_text(label_message, "Password contains a common pattern,\nRemove it to continue\nEg: '123','password','qwerty','0000',etc.", "red", speed=15)
            return
        elif "#" not in paswd:
            type_text(label_message, "Password must contain a '#'", "red", speed=15)
            return
        elif "@" not in paswd:
            type_text(label_message, "Password must contain an '@'", "red", speed=15)
            return
        elif "&" not in paswd:
            type_text(label_message, "Password must contain a '&'", "red", speed=15)
            return
        elif not any(char.isdigit() for char in paswd):
            type_text(label_message, "Password must contain a number", "red", speed=15)
            return
        elif total != 25:
            type_text(label_message, "The digits in the password must add\nup to 25", "red", speed=15)
            return
        elif "!" not in paswd:
            type_text(label_message, "Password must contain an exclamation mark", "red", speed=15)
            return
        elif "*" not in paswd:
            type_text(label_message, "Password must contain a '*'", "red", speed=15)
            return
        elif "%" not in paswd:
            type_text(label_message, "Password must contain a '%'", "red", speed=15)
            return
        elif "?" not in paswd:
            type_text(label_message, "Password must contain a question mark", "red", speed=15)
            return
        
        step = 1  
        label_name.pack_forget()
        entry_name_canvas.pack_forget()
        label_pass.pack_forget()
        entry_pass_frame.pack_forget()
        label_welcome.pack_forget()
        
        type_text(label_message,f"Validating your details...", "yellow", speed=25)
        show_watermark(True)

        def show_success():
            rgb_animation(label_message, text="Account Creation Successful", font=("Segoe UI", 24, "bold"))
            show_watermark(True)

        root.after(1500, show_success)
        step = 2

    elif step == 2:
        type_text(
            label_message,
            "Thank you So Much\nFor Playing",
            color="lime",
            font=("Segoe UI", 24, "bold"),
            speed=50)
        typing_duration = len("Thank you So Much\nFor Playing") * 50

        def start_blink():
            blink_text(label_message, "lime", "white", 600)

        root.after(typing_duration + 200, start_blink)

        btn_continue_canvas.itemconfig(btn_continue_text, text="Exit")
        step = 3
 
    elif step == 3:
        root.quit()  # Exit the application

def blink_text(widget, color1="lime", color2="white", delay=500):
    def toggle():
        current_color = widget.cget("fg")
        new_color = color1 if current_color == color2 else color2
        widget.config(fg=new_color)
        widget.after(delay, toggle)

    toggle()

# ---------- UI SETUP ----------

root = tk.Tk()
root.title("Lino's Password Game")
root.geometry("650x450")
root.configure(bg="#121212")

frame = tk.Frame(root, bg="#1e1e1e")
frame.pack(expand=True, fill="both")

center_frame = tk.Frame(frame, bg="#1e1e1e")
center_frame.place(relx=0.5, rely=0.4, anchor="center")

# Welcome label
label_welcome = tk.Label(center_frame, text="Welcome to Lino's Password Game",
                         font=("Segoe UI", 18, "bold"), bg="#1e1e1e", fg="lime")
label_welcome.pack(pady=15)

# Name input
label_name = tk.Label(center_frame, text="Enter your name:", font=("Segoe UI", 12, "bold"), bg="#1e1e1e", fg="white")
label_name.pack()
entry_name_canvas = tk.Canvas(center_frame, width=350, height=40, bg="#1e1e1e", highlightthickness=0)
entry_name_canvas.pack(pady=8)
round_rectangle(entry_name_canvas, 0, 0, 350, 40, radius=20, fill="#2b2b2b", outline="#2b2b2b")
entry_name = tk.Entry(entry_name_canvas, width=30, font=("Segoe UI", 12, "bold"),
                      bg="#2b2b2b", fg="white", insertbackground="white", relief="flat")
entry_name.place(x=15, y=7)

# Password input
label_pass = tk.Label(center_frame, text="Create your password:", font=("Segoe UI", 12, "bold"), bg="#1e1e1e", fg="white")
label_pass.pack()
entry_pass_frame = tk.Frame(center_frame, bg="#1e1e1e")
entry_pass_frame.pack(pady=8)

entry_pass_canvas = tk.Canvas(entry_pass_frame, width=250, height=40, bg="#1e1e1e", highlightthickness=0)
entry_pass_canvas.pack(side="left")
round_rectangle(entry_pass_canvas, 0, 0, 250, 40, radius=20, fill="#2b2b2b", outline="#2b2b2b")
entry_pass = tk.Entry(entry_pass_canvas, width=20, font=("Segoe UI", 12, "bold"),
                      bg="#2b2b2b", fg="white", insertbackground="white", relief="flat", show="")
entry_pass.place(x=15, y=7)

btn_toggle_canvas = tk.Canvas(entry_pass_frame, width=70, height=40, bg="#1e1e1e", highlightthickness=0)
btn_toggle_canvas.pack(side="right", padx=8)
round_rectangle(btn_toggle_canvas, 0, 0, 70, 40, radius=20, fill="white", outline="white", tags="btn_toggle")
btn_toggle_text = btn_toggle_canvas.create_text(35, 20, text="Hide", fill="black", font=("Segoe UI", 9, "bold"), tags="btn_toggle_text")
btn_toggle_canvas.tag_bind("btn_toggle", "<Button-1>", lambda e: toggle_password())
btn_toggle_canvas.tag_bind("btn_toggle_text", "<Button-1>", lambda e: toggle_password())

# Message label
label_message = tk.Label(center_frame, text="", font=("Courier New", 24, "bold"), bg="#1e1e1e", fg="white", justify="center")
label_message.pack(pady=20)

# Continue button
btn_continue_canvas = tk.Canvas(frame, width=200, height=45, bg="#1e1e1e", highlightthickness=0)
round_rectangle(btn_continue_canvas, 0, 0, 200, 45, radius=22, fill="lime", outline="lime", tags="btn")
btn_continue_text = btn_continue_canvas.create_text(100, 22, text="Continue", fill="black", font=("Segoe UI", 13, "bold"), tags="btn_text")

def on_continue_click(event):
    if not is_animating:
        create_account()

btn_continue_canvas.tag_bind("btn", "<Button-1>", on_continue_click)
btn_continue_canvas.tag_bind("btn_text", "<Button-1>", on_continue_click)

btn_continue_canvas.place(relx=0.5, rely=0.92, anchor="center")

hovering = False
color_steps = 20
current_step = 0

def interpolate_color(start, end, step, max_steps):
    return tuple(
        int(start[i] + (float(end[i] - start[i]) * step / max_steps))
        for i in range(3)
    )

def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb

#Colors of button
lime_rgb = (0, 255, 0)        
white_rgb = (255, 255, 255)   

def animate_to_white():
    global current_step
    if hovering and current_step < color_steps:
        current_step += 1
        new_color = interpolate_color(lime_rgb, white_rgb, current_step, color_steps)
        hex_color = rgb_to_hex(new_color)
        btn_continue_canvas.itemconfig("btn", fill=hex_color, outline=hex_color)
        btn_continue_canvas.after(20, animate_to_white)

def animate_to_lime():
    global current_step
    if not hovering and current_step > 0:
        current_step -= 1
        new_color = interpolate_color(lime_rgb, white_rgb, current_step, color_steps)
        hex_color = rgb_to_hex(new_color)
        btn_continue_canvas.itemconfig("btn", fill=hex_color, outline=hex_color)
        btn_continue_canvas.after(20, animate_to_lime)
    elif current_step == 0:
        btn_continue_canvas.itemconfig("btn", fill=rgb_to_hex(lime_rgb), outline=rgb_to_hex(lime_rgb))

def on_hover_enter(event):
    global hovering
    hovering = True
    animate_to_white()

def on_hover_leave(event):
    global hovering
    hovering = False
    animate_to_lime()

btn_continue_canvas.tag_bind("btn", "<Enter>", on_hover_enter)
btn_continue_canvas.tag_bind("btn_text", "<Enter>", on_hover_enter)
btn_continue_canvas.tag_bind("btn", "<Leave>", on_hover_leave)
btn_continue_canvas.tag_bind("btn_text", "<Leave>", on_hover_leave)

watermark = tk.Label(frame, text="By Lino", font=("Segoe UI", 10, "bold"), fg="lime", bg="#1e1e1e")
watermark2 = tk.Label(frame, text="v1.0", font=("Segoe UI", 10), fg="white", bg="#1e1e1e")

# Start the app
root.mainloop()
