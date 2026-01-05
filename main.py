from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
import time


class TimerApp(App):
    """
    A simple timer application with:
    - Start / Pause / Reset controls
    - Real-time elapsed time display
    - Checkpoints that show the time difference between segments
    """

    def build(self):
        # Timer state variables
        self.start_time = 0            # Timestamp when the timer started
        self.last_checkpoint = 0       # Timestamp of the last checkpoint
        self.running = False           # Whether the timer is currently running
        self.paused = False            # Whether the timer is paused
        self.checkpoint_count = 0      # Number of checkpoints recorded
        self.pause_time = 0            # Timestamp when pause started
        self.pause_offset = 0          # Total paused time to subtract

        # Main layout
        layout = BoxLayout(orientation='vertical')

        # Timer display
        self.timer_label = Label(text="00:00", font_size=40)
        layout.add_widget(self.timer_label)

        # Buttons row
        button_layout = BoxLayout()

        self.start_button = Button(text="Start", on_press=self.start_timer)
        self.pause_button = Button(text="Pause", on_press=self.pause_timer)
        self.checkpoint_button = Button(text="Checkpoint", on_press=self.mark_checkpoint)
        self.reset_button = Button(text="Reset", on_press=self.reset_timer)

        button_layout.add_widget(self.start_button)
        button_layout.add_widget(self.pause_button)
        button_layout.add_widget(self.checkpoint_button)
        button_layout.add_widget(self.reset_button)

        layout.add_widget(button_layout)

        # Log area for checkpoints
        self.log_text = TextInput(readonly=True, size_hint_y=2)
        layout.add_widget(self.log_text)

        return layout

    def start_timer(self, instance):
        """
        Starts the timer. If resuming from pause, adjusts pause offset.
        """
        if not self.running:
            if self.paused:
                # Resuming from pause
                self.pause_offset += time.time() - self.pause_time
            else:
                # Starting fresh
                self.start_time = time.time()
                self.last_checkpoint = self.start_time
                self.checkpoint_count = 0
                self.pause_offset = 0

            self.running = True
            self.paused = False
            self.update_timer()

    def update_timer(self):
        """
        Updates the timer display every 0.1 seconds while running.
        """
        if self.running:
            elapsed = time.time() - self.start_time - self.pause_offset
            self.timer_label.text = self.format_time(elapsed)

            # Schedule next update
            Clock.schedule_once(lambda dt: self.update_timer(), 0.1)

    def pause_timer(self, instance):
        """
        Pauses the timer and stores the pause timestamp.
        """
        if self.running:
            self.running = False
            self.paused = True
            self.pause_time = time.time()

    def mark_checkpoint(self, instance):
        """
        Records a checkpoint and logs the time difference since the last one.
        """
        if not self.running:
            return  # Do not allow checkpoints while paused or stopped

        self.checkpoint_count += 1

        # Current time adjusted for pauses
        now = time.time() - self.pause_offset

        # Time difference since last checkpoint
        delta = now - self.last_checkpoint
        self.last_checkpoint = now

        # Append to log
        self.log_text.text += f"Checkpoint {self.checkpoint_count}: {self.format_time(delta)}\n"

    def reset_timer(self, instance):
        """
        Resets the timer and clears all state.
        """
        self.running = False
        self.paused = False
        self.timer_label.text = "00:00"
        self.log_text.text = ""
        self.checkpoint_count = 0
        self.start_time = 0
        self.last_checkpoint = 0
        self.pause_time = 0
        self.pause_offset = 0

    def format_time(self, seconds):
        """
        Converts seconds into MM:SS format.
        """
        minutes = int(seconds) // 60
        sec = int(seconds) % 60
        return f"{minutes:02}:{sec:02}"


if __name__ == '__main__':
    TimerApp().run()
