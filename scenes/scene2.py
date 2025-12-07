from manim import *
import numpy as np

class CircleDetectionScene(Scene):
    def construct(self):
        # Title
        title = Text("Finding the Pattern Center", font_size=48, color=BLUE)
        self.play(Write(title), run_time=1.5)
        self.wait(1)
        self.play(FadeOut(title), run_time=0.5)
        
        # Method 1 - Hough Circles (brief mention)
        method1_text = Text("Method 1: Hough Circle Detection", font_size=36, color=YELLOW)
        method1_text.to_edge(UP)
        self.play(Write(method1_text), run_time=1)
        
        # Show brief code snippet
        code1_text = """circles = cv2.HoughCircles(
    blurred_image, 
    cv2.HOUGH_GRADIENT,
    dp=1, minDist=50,
    param1=100, param2=30,
    minRadius=100, maxRadius=400
)"""
        code1 = Code(
            code_string=code1_text,
            language="python",
            tab_width=4,
            background="window",
            formatter_style="monokai"
        ).scale(0.7)
        
        self.play(FadeIn(code1), run_time=1)
        self.wait(2)  # NARRATION: "First, we try automatic detection using Hough Circles"
        self.play(FadeOut(code1), run_time=0.5)
        
        # Transition to fallback method
        fallback_text = Text("Fallback: Manual 3-Point Method", font_size=36, color=GREEN)
        fallback_text.to_edge(UP)
        self.play(Transform(method1_text, fallback_text), run_time=1)
        self.wait(1)  # NARRATION: "If that fails, we use a geometric approach"
        
        self.play(FadeOut(method1_text), run_time=0.5)
        
        # Mathematical principle
        principle = Text(
            "3 non-collinear points → unique circle",
            font_size=32,
            color=BLUE_C
        ).to_edge(UP)
        self.play(Write(principle), run_time=1.5)
        self.wait(2)  # NARRATION: "Based on the fact that 3 non-collinear points define a unique circle"
        
        # Create three points
        p1 = np.array([-2, -1, 0])
        p2 = np.array([3, -0.5, 0])
        p3 = np.array([0.5, 2.5, 0])
        
        # Create dot objects
        dot1 = Dot(p1, color=RED, radius=0.12)
        dot2 = Dot(p2, color=RED, radius=0.12)
        dot3 = Dot(p3, color=RED, radius=0.12)
        
        # Labels for points - adjust P3 position to avoid overlap
        label1 = MathTex("P_1", color=RED).next_to(dot1, DOWN, buff=0.2)
        label2 = MathTex("P_2", color=RED).next_to(dot2, DOWN, buff=0.2)
        label3 = MathTex("P_3", color=RED).next_to(dot3, LEFT, buff=0.25)  # Changed to LEFT to avoid overlap
        
        # Animate points appearing one by one - SLOWER pace
        self.play(FadeIn(dot1, scale=0.5), Write(label1), run_time=1)
        self.wait(0.5)
        self.play(FadeIn(dot2, scale=0.5), Write(label2), run_time=1)
        self.wait(0.5)
        self.play(FadeIn(dot3, scale=0.5), Write(label3), run_time=1)
        self.wait(1.5)  # NARRATION: "We select three points on the container rim"
        
        # Draw triangle - slower
        triangle = Polygon(p1, p2, p3, color=YELLOW, stroke_width=3)
        self.play(Create(triangle), run_time=2)
        self.wait(2)  # NARRATION: "Connect them to form a triangle"
        
        # Calculate actual circle parameters
        # Using the formula from the code
        D = 2 * (p1[0] * (p2[1] - p3[1]) + p2[0] * (p3[1] - p1[1]) + p3[0] * (p1[1] - p2[1]))
        ux = ((p1[0]**2 + p1[1]**2) * (p2[1] - p3[1]) + 
              (p2[0]**2 + p2[1]**2) * (p3[1] - p1[1]) + 
              (p3[0]**2 + p3[1]**2) * (p1[1] - p2[1])) / D
        uy = ((p1[0]**2 + p1[1]**2) * (p3[0] - p2[0]) + 
              (p2[0]**2 + p2[1]**2) * (p1[0] - p3[0]) + 
              (p3[0]**2 + p3[1]**2) * (p2[0] - p1[0])) / D
        
        center = np.array([ux, uy, 0])
        radius = np.sqrt((p1[0] - ux)**2 + (p1[1] - uy)**2)
        
        # Draw the circumcircle - slower
        circle = Circle(radius=radius, color=BLUE, stroke_width=4).move_to(center)
        self.play(Create(circle), run_time=2.5)
        self.wait(2)  # NARRATION: "And calculate the unique circle passing through all three points"
        
        # Highlight the center
        center_dot = Dot(center, color=GREEN, radius=0.15)
        center_label = Text("Center", font_size=28, color=GREEN).next_to(center_dot, RIGHT, buff=0.3)
        
        # Draw radii from center to points
        radius1 = Line(center, p1, color=GREEN_A, stroke_width=2)
        radius2 = Line(center, p2, color=GREEN_A, stroke_width=2)
        radius3 = Line(center, p3, color=GREEN_A, stroke_width=2)
        
        self.play(
            Create(radius1),
            Create(radius2),
            Create(radius3),
            run_time=1.5
        )
        self.play(
            FadeIn(center_dot, scale=0.5),
            Write(center_label),
            run_time=1
        )
        self.wait(2)  # NARRATION: "This gives us the exact center of the pattern"
        
        # Fade out everything except the center
        self.play(
            FadeOut(triangle),
            FadeOut(radius1),
            FadeOut(radius2),
            FadeOut(radius3),
            FadeOut(label1),
            FadeOut(label2),
            FadeOut(label3),
            FadeOut(principle),
            run_time=1
        )
        
        # Pulse the center to emphasize it
        self.play(
            center_dot.animate.scale(1.5),
            run_time=0.5
        )
        self.play(
            center_dot.animate.scale(1/1.5),
            run_time=0.5
        )
        self.wait(1)
        
        # Show the Python code
        self.play(
            FadeOut(dot1),
            FadeOut(dot2),
            FadeOut(dot3),
            FadeOut(circle),
            FadeOut(center_dot),
            FadeOut(center_label),
            run_time=0.8
        )
        
        code_title = Text("Python Implementation", font_size=36, color=BLUE)
        code_title.to_edge(UP)
        self.play(Write(code_title), run_time=1)
        
        # Show the actual code
        python_code_text = """def calculate_circle_from_points(points):
    p1, p2, p3 = points
    
    D = 2 * (p1[0] * (p2[1] - p3[1]) + 
             p2[0] * (p3[1] - p1[1]) + 
             p3[0] * (p1[1] - p2[1]))
    
    ux = ((p1[0]**2 + p1[1]**2) * (p2[1] - p3[1]) +
          (p2[0]**2 + p2[1]**2) * (p3[1] - p1[1]) +
          (p3[0]**2 + p3[1]**2) * (p1[1] - p2[1])) / D
    
    uy = ((p1[0]**2 + p1[1]**2) * (p3[0] - p2[0]) +
          (p2[0]**2 + p2[1]**2) * (p1[0] - p3[0]) +
          (p3[0]**2 + p3[1]**2) * (p2[0] - p1[0])) / D
    
    center = (int(ux), int(uy))
    radius = int(np.sqrt((p1[0]-ux)**2 + (p1[1]-uy)**2))
    
    return center, radius"""
        
        python_code = Code(
            code_string=python_code_text,
            language="python",
            tab_width=4,
            background="window",
            formatter_style="monokai"
        ).scale(0.65).shift(DOWN * 0.3)
        
        self.play(FadeIn(python_code, shift=UP), run_time=1.5)
        self.wait(3)  # NARRATION: "Here's the Python implementation using the circumcircle formula"
        
        # Fade everything out
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=1
        )
