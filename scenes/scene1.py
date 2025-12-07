from manim import *
import numpy as np
from PIL import Image

class IntroSceneWithTitles(Scene):
    def construct(self):
        # Main title card
        main_title = Text("Analyzing Nitrogen-Water Instabilities", font_size=48, color=BLUE, weight=BOLD)
        subtitle = Text("For The Scientific Computing Course Project", font_size=32, color=WHITE)
        subtitle2 = Text("By: Ayman Alashkar", font_size=26, color=YELLOW_E)
        title_group = VGroup(main_title, subtitle, subtitle2).arrange(DOWN, buff=0.5)
        
        self.play(Write(main_title), run_time=1.5)
        self.play(FadeIn(subtitle, shift=UP), run_time=1)
        self.play(FadeIn(subtitle2, shift=UP), run_time=1)
        self.wait(2)  # NARRATION: Introduction
        self.play(FadeOut(title_group), run_time=0.8)
        
        # Section title
        section_title = Text("The Experimental Setup", font_size=36, color=YELLOW)
        section_title.to_edge(UP, buff=0.3)
        self.play(Write(section_title), run_time=1)
        
        # Load and prepare the experimental image
        img_path = "data/d4_T20_1.JPG"
        img = ImageMobject(img_path)
        
        # Scale image to fit nicely on screen
        img.height = 5
        img.shift(DOWN * 0.3)
        
        # Fade in the experimental image
        self.play(FadeIn(img), run_time=1.5)
        self.wait(3)  # NARRATION: "Pouring liquid nitrogen over water"
        
        # Update section title
        self.play(
            Transform(section_title, Text("Sampling Strategy", font_size=36, color=YELLOW).to_edge(UP, buff=0.3)),
            run_time=0.8
        )
        
        # Define the circular strip parameters
        container_radius = img.height * 0.38
        strip_width = 0.15
        
        # Create the circular strip
        outer_circle = Circle(
            radius=container_radius + strip_width/2, 
            color=YELLOW, 
            stroke_width=8
        ).shift(DOWN * 0.3)
        inner_circle = Circle(
            radius=container_radius - strip_width/2, 
            color=YELLOW, 
            stroke_width=8
        ).shift(DOWN * 0.3)
        
        self.play(
            Create(outer_circle),
            Create(inner_circle),
            run_time=2
        )
        self.wait(3)  # NARRATION: "Sampling intensity at a specific radius"
        
        # Highlight the strip region
        strip_region = Annulus(
            inner_radius=container_radius - strip_width/2,
            outer_radius=container_radius + strip_width/2,
            color=YELLOW,
            fill_opacity=0.25,
            stroke_width=0
        ).shift(DOWN * 0.3)
        self.play(FadeIn(strip_region), run_time=0.8)
        self.wait(1.5)
        
        # Update section title
        self.play(
            Transform(section_title, Text("From Circular to Linear", font_size=36, color=YELLOW).to_edge(UP, buff=0.3)),
            run_time=0.8
        )
        
        self.play(FadeOut(img), run_time=1)
        
        # Unwrap the strip
        unwrapped_strip = Rectangle(
            width=8,
            height=0.6,
            color=YELLOW,
            fill_opacity=0.25,
            stroke_width=6
        ).shift(DOWN * 1.5)
        
        self.play(
            Transform(outer_circle, unwrapped_strip.copy()),
            Transform(inner_circle, unwrapped_strip.copy()),
            Transform(strip_region, unwrapped_strip.copy().set_opacity(0.25)),
            run_time=2
        )
        self.wait(2.5)  # NARRATION: "Unwrap into linear signal"
        
        # Create intensity profile
        n_points = 200
        theta = np.linspace(0, 2*np.pi, n_points)
        intensity = 0.5 + 0.3 * np.sin(8 * theta) + 0.15 * np.sin(16 * theta - 0.5) + 0.1 * np.random.randn(n_points) * 0.3
        intensity = (intensity - intensity.min()) / (intensity.max() - intensity.min())
        
        # Update section title
        self.play(
            Transform(section_title, Text("Intensity Signal", font_size=36, color=YELLOW).to_edge(UP, buff=0.3)),
            run_time=0.8
        )
        
        # Create axes
        axes = Axes(
            x_range=[0, 2*np.pi, np.pi/2],
            y_range=[0, 1, 0.5],
            x_length=8,
            y_length=2,
            axis_config={"color": BLUE_D, "include_tip": False},
            x_axis_config={"numbers_to_include": []},
            y_axis_config={"numbers_to_include": []},
        ).shift(DOWN * 1.5)
        
        intensity_curve = axes.plot_line_graph(
            x_values=theta,
            y_values=intensity,
            line_color=YELLOW,
            stroke_width=4,
            add_vertex_dots=False
        )
        
        self.play(
            FadeOut(outer_circle),
            FadeOut(inner_circle),
            FadeOut(strip_region),
            Create(axes),
            run_time=1
        )
        
        self.play(Create(intensity_curve), run_time=2.5)
        self.wait(1)
        
        # Add axis labels
        angle_label = MathTex(r"\theta", color=WHITE).next_to(axes.x_axis, RIGHT, buff=0.2).scale(0.8)
        intensity_label = MathTex(r"I", color=WHITE).next_to(axes.y_axis, UP, buff=0.2).scale(0.8)
        
        self.play(
            Write(angle_label),
            Write(intensity_label),
            run_time=0.8
        )
        self.wait(3)  # NARRATION: "Intensity profile ready for analysis"
        
        # Fade everything out
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=1
        )
