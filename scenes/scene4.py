from manim import *
import numpy as np

class ResultsScene(Scene):
    def construct(self):
        # Title
        title = Text("The Result: Intensity vs Angle", font_size=42, color=BLUE)
        self.play(Write(title), run_time=1.5)
        self.wait(1)
        self.play(title.animate.scale(0.65).to_edge(UP, buff=0.2), run_time=0.8)

        # Create axes
        axes = Axes(
            x_range=[0, 360, 60],
            y_range=[50, 210, 50],
            x_length=10,
            y_length=5,
            axis_config={
                "color": BLUE_D,
                "include_tip": True,
                "include_numbers": True,
                "font_size": 28
            },
            x_axis_config={
                "numbers_to_include": [0, 60, 120, 180, 240, 300, 360]
            },
            y_axis_config={
                "numbers_to_include": [50, 100, 150, 200]
            }
        ).shift(RIGHT * 0.8 + UP * 0.3)
        
        # Axis labels
        x_label = Text("Angle (degrees)", font_size=30).next_to(axes.x_axis, DOWN, buff=0.2)
        y_label = Text("Average Intensity", font_size=30).next_to(axes.y_axis, LEFT, buff=0.1).rotate(90 * DEGREES)
        
        self.play(Create(axes), run_time=1.5)
        self.play(Write(x_label), Write(y_label), run_time=1)
        self.wait(1)  # NARRATION: "Here's the final result - intensity as a function of angle"
        
        # Generate realistic intensity data with oscillations (finger pattern)
        np.random.seed(42)
        n_points = 200
        angles = np.linspace(0, 360, n_points)
        
        # Create oscillating pattern with ~8 fingers (peaks)
        n_fingers = 8
        base_intensity = 130
        amplitude = 25
        noise_level = 8
        
        # Main oscillation + harmonics + noise
        intensity = (base_intensity + 
                    amplitude * np.sin(n_fingers * angles * np.pi / 180) +
                    amplitude * 0.3 * np.sin(2 * n_fingers * angles * np.pi / 180 - 0.5) +
                    noise_level * np.random.randn(n_points))
        
        # Smooth the noise a bit
        from scipy.ndimage import gaussian_filter1d
        intensity = gaussian_filter1d(intensity, sigma=2)
        
        # Create the plot
        plot = axes.plot_line_graph(
            x_values=angles,
            y_values=intensity,
            line_color=YELLOW,
            stroke_width=3,
            add_vertex_dots=False
        )
        
        # Animate drawing the curve from left to right
        self.play(Create(plot), run_time=4, rate_func=linear)
        self.wait(2)  # NARRATION: "Notice the oscillating pattern - these peaks represent the finger structures"
        
        # Highlight a few peaks
        peak_indices = []
        for i in range(1, len(intensity) - 1):
            if intensity[i] > intensity[i-1] and intensity[i] > intensity[i+1]:
                if intensity[i] > base_intensity + amplitude * 0.3:  # Only significant peaks
                    peak_indices.append(i)
        
        # Mark some peaks
        peak_dots = VGroup()
        for idx in peak_indices:  # Every other peak to avoid crowding
            if idx < len(angles):
                peak_dot = Dot(
                    axes.c2p(angles[idx], intensity[idx]),
                    color=RED,
                    radius=0.08
                )
                peak_dots.add(peak_dot)
        
        self.play(FadeIn(peak_dots, lag_ratio=0.1), run_time=1.5)
        self.wait(1.5)  # NARRATION: "Each peak corresponds to a finger in the instability pattern"
        
        # Add annotation
        finger_count = Text(f"~{n_fingers} fingers detected", font_size=28, color=GREEN)
        finger_count.to_edge(RIGHT, buff=1).shift(UP * 2)
        self.play(FadeIn(finger_count, shift=LEFT), run_time=1)
        self.wait(2)
        
        # Fade out everything except title
        self.play(
            FadeOut(axes),
            FadeOut(x_label),
            FadeOut(y_label),
            FadeOut(plot),
            FadeOut(peak_dots),
            FadeOut(finger_count),
            run_time=1
        )
        
        # THANK YOU
        thank_you = VGroup(
            Text("Thank You!", font_size=72, color=BLUE, weight=BOLD),
            Text("Questions?", font_size=40, color=WHITE)
        ).arrange(DOWN, buff=0.8)
        
        self.play(
            FadeOut(title),
            run_time=0.5
        )
        self.play(Write(thank_you[0]), run_time=1.5)
        self.wait(0.5)
        self.play(FadeIn(thank_you[1], shift=UP), run_time=1)
        self.wait(3)
        
        # Final fade
        self.play(FadeOut(thank_you), run_time=1.5)