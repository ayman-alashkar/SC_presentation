from manim import *
import numpy as np

class PolarTransformScene(Scene):
    def construct(self):
        # Title
        title = Text("From Pixels to Polar Coordinates", font_size=44, color=BLUE)
        self.play(Write(title), run_time=1.5)
        self.wait(1)
        self.play(title.animate.scale(0.65).to_edge(UP, buff=0.2), run_time=0.8)  # Smaller and higher
        
        # ===== PART 1: Cartesian Grid with Pixels =====
        subtitle1 = Text("Cartesian Space: Pixels as Intensity Values", font_size=26, color=YELLOW)
        subtitle1.next_to(title, DOWN, buff=0.2)  # Closer to title
        self.play(Write(subtitle1), run_time=1)
        self.wait(1.5)  # NARRATION: "Each pixel represents an intensity value in Cartesian coordinates"
        
        # Create a Cartesian grid
        grid_size = 7
        cell_size = 0.6
        
        # Create grid lines
        grid = VGroup()
        for i in range(grid_size + 1):
            # Vertical lines
            v_line = Line(
                [i * cell_size - grid_size * cell_size / 2, -grid_size * cell_size / 2, 0],
                [i * cell_size - grid_size * cell_size / 2, grid_size * cell_size / 2, 0],
                color=GRAY, stroke_width=1
            )
            grid.add(v_line)
            
            # Horizontal lines
            h_line = Line(
                [-grid_size * cell_size / 2, i * cell_size - grid_size * cell_size / 2, 0],
                [grid_size * cell_size / 2, i * cell_size - grid_size * cell_size / 2, 0],
                color=GRAY, stroke_width=1
            )
            grid.add(h_line)
        
        # Create dots representing pixels (one per cell)
        pixels = VGroup()
        np.random.seed(42)
        for i in range(grid_size):
            for j in range(grid_size):
                x = (i + 0.5) * cell_size - grid_size * cell_size / 2
                y = (j + 0.5) * cell_size - grid_size * cell_size / 2
                # Vary dot size slightly to represent different intensities
                intensity = np.random.uniform(0.5, 1.0)
                dot = Dot([x, y, 0], radius=0.08 * intensity, color=interpolate_color(BLUE_E, WHITE, intensity))
                pixels.add(dot)
        
        self.play(Create(grid), run_time=1.5)
        self.play(FadeIn(pixels, lag_ratio=0.02), run_time=2)
        self.wait(2)  # NARRATION: "Arranged in a regular Cartesian grid"
        
        # ===== PART 2: Show circular strip passing through grid =====
        self.play(FadeOut(subtitle1), run_time=0.5)
        subtitle2 = Text("Sampling a Circular Strip", font_size=28, color=YELLOW)
        subtitle2.next_to(title, DOWN, buff=0.3)
        self.play(Write(subtitle2), run_time=1)
        
        # Draw circular strip - THINNER to show the problem clearly
        center = ORIGIN
        radius = 1.8
        strip_width = 0.25  # Reduced from 0.4 to make it thinner
        
        outer_circle = Circle(radius=radius + strip_width/2, color=YELLOW, stroke_width=3)
        inner_circle = Circle(radius=radius - strip_width/2, color=YELLOW, stroke_width=3)
        strip_fill = Annulus(
            inner_radius=radius - strip_width/2,
            outer_radius=radius + strip_width/2,
            color=YELLOW,
            fill_opacity=0.2,
            stroke_width=0
        )
        
        self.play(Create(outer_circle), Create(inner_circle), run_time=1.5)
        self.play(FadeIn(strip_fill), run_time=0.8)
        self.wait(2)  # NARRATION: "But our circular strip doesn't align with the Cartesian grid"
        
        # Highlight pixels that fall in the strip
        strip_pixels = VGroup()
        for dot in pixels:
            dist = np.linalg.norm(dot.get_center()[:2])
            if radius - strip_width/2 <= dist <= radius + strip_width/2:
                strip_pixels.add(dot)
        
        self.play(
            *[dot.animate.set_color(RED).scale(1.3) for dot in strip_pixels],
            run_time=1.5
        )
        self.wait(2)  # NARRATION: "Making it difficult to extract accurate intensity values"
        
        # ===== PART 3: Polar Transformation =====
        self.play(
            FadeOut(subtitle2),
            FadeOut(grid),
            FadeOut(pixels),
            FadeOut(outer_circle),
            FadeOut(inner_circle),
            FadeOut(strip_fill),
            run_time=1
        )
        
        subtitle3 = Text("Solution: Transform to Polar Coordinates", font_size=28, color=GREEN)
        subtitle3.next_to(title, DOWN, buff=0.3)
        self.play(Write(subtitle3), run_time=1)
        self.wait(1.5)  # NARRATION: "So we transform to polar coordinates"
        
        # Show transformation code
        transform_code_text = """y, x = np.indices(image_gray.shape)

r = np.sqrt((x - center[0])**2 + (y - center[1])**2)
theta = np.arctan2(y - center[1], x - center[0])
theta_deg = (np.degrees(theta) + 360) % 360

half_width = strip_width / 2
strip_mask = (r >= radius - half_width) & 
             (r <= radius + half_width)

theta_strip = theta_deg[strip_mask]
intensity_strip = image_gray[strip_mask]"""
        
        transform_code = Code(
            code_string=transform_code_text,
            language="python",
            tab_width=4,
            background="window",
            formatter_style="monokai"
        ).scale(0.55).shift(DOWN * 0.5)
        
        self.play(FadeOut(subtitle3), run_time=0.5)
        
        # ===== COORDINATE TRANSFORMATION WITH LABELED ANIMATION =====
        transform_title = Text("Coordinate Transformation", font_size=30, color=ORANGE)
        transform_title.next_to(title, DOWN, buff=0.2)
        self.play(Write(transform_title), run_time=1)
        
        # Show transformation code FIRST
        transform_code_text = """y, x = np.indices(image_gray.shape)

r = np.sqrt((x - center[0])**2 + (y - center[1])**2)
theta = np.arctan2(y - center[1], x - center[0])
theta_deg = (np.degrees(theta) + 360) % 360

half_width = strip_width / 2
strip_mask = (r >= radius - half_width) & 
             (r <= radius + half_width)

theta_strip = theta_deg[strip_mask]
intensity_strip = image_gray[strip_mask]"""
        
        transform_code = Code(
            code_string=transform_code_text,
            language="python",
            tab_width=4,
            background="window",
            formatter_style="monokai"
        ).scale(0.5).to_edge(LEFT, buff=0.3).shift(DOWN * 0.5)
        
        self.play(FadeIn(transform_code, shift=UP), run_time=1.5)
        self.wait(2.5)  # NARRATION: "Using this transformation"
        
        # Now show the GRID TRANSFORMATION on the RIGHT
        # Cartesian grid with axes
        offset_right_grid = RIGHT * 3 + DOWN * 0.5
        cart_grid_size = 5
        cart_cell_size = 0.5
        cart_grid_anim = VGroup()
        
        for i in range(cart_grid_size + 1):
            # Vertical lines
            v_line = Line(
                offset_right_grid + [i * cart_cell_size - cart_grid_size * cart_cell_size / 2, -cart_grid_size * cart_cell_size / 2, 0],
                offset_right_grid + [i * cart_cell_size - cart_grid_size * cart_cell_size / 2, cart_grid_size * cart_cell_size / 2, 0],
                color=BLUE_D, stroke_width=2
            )
            cart_grid_anim.add(v_line)
            
            # Horizontal lines
            h_line = Line(
                offset_right_grid + [-cart_grid_size * cart_cell_size / 2, i * cart_cell_size - cart_grid_size * cart_cell_size / 2, 0],
                offset_right_grid + [cart_grid_size * cart_cell_size / 2, i * cart_cell_size - cart_grid_size * cart_cell_size / 2, 0],
                color=BLUE_D, stroke_width=2
            )
            cart_grid_anim.add(h_line)
        
        # Axis labels: x at BOTTOM, y at LEFT
        x_axis_label = MathTex("x", color=WHITE).next_to(
            offset_right_grid + DOWN * cart_grid_size * cart_cell_size / 2, DOWN, buff=0.2
        ).scale(0.8)
        y_axis_label = MathTex("y", color=WHITE).next_to(
            offset_right_grid + LEFT * cart_grid_size * cart_cell_size / 2, LEFT, buff=0.2
        ).scale(0.8)
        
        self.play(Create(cart_grid_anim), Write(x_axis_label), Write(y_axis_label), run_time=1.5)
        self.wait(1.5)
        
        # Create POLAR grid (target) with labels
        polar_grid_anim = VGroup()
        n_radial_labeled = 8
        n_circles_labeled = 4
        polar_radius_anim = 1.3
        
        # Radial lines with theta labels
        theta_labels = VGroup()
        for i in range(n_radial_labeled):
            angle = i * 2 * np.pi / n_radial_labeled
            line = Line(
                offset_right_grid,
                offset_right_grid + polar_radius_anim * np.array([np.cos(angle), np.sin(angle), 0]),
                color=ORANGE, stroke_width=2
            )
            polar_grid_anim.add(line)
            
            # Label every other radial line to avoid crowding
            if i % 2 == 0:
                label_pos = offset_right_grid + (polar_radius_anim + 0.35) * np.array([np.cos(angle), np.sin(angle), 0])
                theta_label = MathTex(f"\\theta_{{{i//2 + 1}}}", color=ORANGE).move_to(label_pos).scale(0.5)
                theta_labels.add(theta_label)
        
        # Concentric circles with r labels
        r_labels = VGroup()
        for i in range(1, n_circles_labeled + 1):
            r = i * polar_radius_anim / n_circles_labeled
            circle = Circle(radius=r, color=ORANGE, stroke_width=2).move_to(offset_right_grid)
            polar_grid_anim.add(circle)
            
            # Label on the right side
            label_pos = offset_right_grid + RIGHT * (r + 0.15)
            r_label = MathTex(f"r_{{{i}}}", color=ORANGE).move_to(label_pos).scale(0.5)
            r_labels.add(r_label)
        
        # TRANSFORM: Cartesian grid morphs into polar grid
        self.play(
            Transform(cart_grid_anim, polar_grid_anim),
            FadeOut(x_axis_label),
            FadeOut(y_axis_label),
            run_time=3
        )
        
        # Add the polar labels
        self.play(
            FadeIn(theta_labels, lag_ratio=0.1),
            FadeIn(r_labels, lag_ratio=0.1),
            run_time=1.5
        )
        self.wait(2.5)  # NARRATION: "The Cartesian grid transforms into polar with radial and angular coordinates"
        
        # Clean up for next section
        self.play(
            FadeOut(transform_code),
            FadeOut(transform_title),
            FadeOut(cart_grid_anim),
            FadeOut(theta_labels),
            FadeOut(r_labels),
            run_time=1
        )
        
        subtitle4 = Text("Comparing the Two Approaches", font_size=26, color=BLUE_C)
        subtitle4.next_to(title, DOWN, buff=0.2)
        self.play(Write(subtitle4), run_time=1)
        
        # LEFT SIDE: Recreate the EXACT same Cartesian grid from the beginning
        left_label = Text("Cartesian (Problem)", font_size=24, color=RED)
        left_label.shift(LEFT * 3.5 + UP * 2.5)  # ABOVE the figure
        
        # Identical to the beginning - same size, same position
        cart_grid_left = VGroup()
        grid_size = 7
        cell_size = 0.6
        offset_left = LEFT * 3.5
        
        for i in range(grid_size + 1):
            v_line = Line(
                offset_left + [i * cell_size - grid_size * cell_size / 2, -grid_size * cell_size / 2, 0],
                offset_left + [i * cell_size - grid_size * cell_size / 2, grid_size * cell_size / 2, 0],
                color=GRAY, stroke_width=1
            )
            cart_grid_left.add(v_line)
            
            h_line = Line(
                offset_left + [-grid_size * cell_size / 2, i * cell_size - grid_size * cell_size / 2, 0],
                offset_left + [grid_size * cell_size / 2, i * cell_size - grid_size * cell_size / 2, 0],
                color=GRAY, stroke_width=1
            )
            cart_grid_left.add(h_line)
        
        # Pixels - identical to beginning
        pixels_cart_left = VGroup()
        np.random.seed(42)
        for i in range(grid_size):
            for j in range(grid_size):
                x = (i + 0.5) * cell_size - grid_size * cell_size / 2
                y = (j + 0.5) * cell_size - grid_size * cell_size / 2
                intensity = np.random.uniform(0.5, 1.0)
                dot = Dot(offset_left + [x, y, 0], radius=0.08 * intensity, 
                         color=interpolate_color(BLUE_E, WHITE, intensity))
                pixels_cart_left.add(dot)
        
        # Circular strip - identical to beginning
        strip_radius_left = 1.8
        strip_width_left = 0.25  # Same thin strip
        strip_outer_left = Circle(radius=strip_radius_left + strip_width_left/2, color=YELLOW, stroke_width=3).shift(offset_left)
        strip_inner_left = Circle(radius=strip_radius_left - strip_width_left/2, color=YELLOW, stroke_width=3).shift(offset_left)
        strip_fill_left = Annulus(
            inner_radius=strip_radius_left - strip_width_left/2,
            outer_radius=strip_radius_left + strip_width_left/2,
            color=YELLOW,
            fill_opacity=0.2,
            stroke_width=0
        ).shift(offset_left)
        
        # Highlight pixels in strip
        strip_pixels_left = VGroup()
        for dot in pixels_cart_left:
            dist = np.linalg.norm((dot.get_center() - offset_left)[:2])
            if strip_radius_left - strip_width_left/2 <= dist <= strip_radius_left + strip_width_left/2:
                strip_pixels_left.add(dot)
        
        self.play(Write(left_label), run_time=0.8)
        self.play(Create(cart_grid_left), run_time=1)
        self.play(FadeIn(pixels_cart_left, lag_ratio=0.02), run_time=1.5)
        self.play(Create(strip_outer_left), Create(strip_inner_left), FadeIn(strip_fill_left), run_time=1)
        self.play(
            *[dot.animate.set_color(RED).scale(1.3) for dot in strip_pixels_left],
            run_time=1
        )
        self.wait(2)  # NARRATION: "On the left: the circular strip on Cartesian grid - poor alignment"
        
        # RIGHT SIDE: Polar grid
        right_label = Text("Polar (Solution)", font_size=24, color=GREEN)
        right_label.shift(RIGHT * 3.5 + UP * 2.5)  # ABOVE the figure
        
        offset_right = RIGHT * 3.5
        polar_grid_right = VGroup()
        n_angle_bins = 12
        radius_display = 1.8
        
        # Radial lines
        for i in range(n_angle_bins):
            angle = i * 2 * np.pi / n_angle_bins
            line = Line(
                offset_right,
                offset_right + radius_display * np.array([np.cos(angle), np.sin(angle), 0]),
                color=BLUE_D,
                stroke_width=1.5
            )
            polar_grid_right.add(line)
        
        # Circular strip in polar
        strip_r_min = radius_display * 0.75
        strip_r_max = radius_display * 0.95
        strip_inner_right = Circle(radius=strip_r_min, color=YELLOW, stroke_width=3).shift(offset_right)
        strip_outer_right = Circle(radius=strip_r_max, color=YELLOW, stroke_width=3).shift(offset_right)
        strip_fill_right = Annulus(
            inner_radius=strip_r_min,
            outer_radius=strip_r_max,
            color=YELLOW,
            fill_opacity=0.2,
            stroke_width=0
        ).shift(offset_right)
        
        self.play(Write(right_label), run_time=0.8)
        self.play(Create(polar_grid_right), run_time=1)
        self.play(Create(strip_inner_right), Create(strip_outer_right), FadeIn(strip_fill_right), run_time=1)
        self.wait(1)
        
        # Show pixels falling into polar cells
        pixels_polar = VGroup()
        np.random.seed(42)
        
        for i in range(n_angle_bins):
            angle_start = i * 2 * np.pi / n_angle_bins
            angle_end = (i + 1) * 2 * np.pi / n_angle_bins
            
            n_pixels = np.random.randint(4, 8)
            for _ in range(n_pixels):
                r = np.random.uniform(strip_r_min, strip_r_max)
                theta = np.random.uniform(angle_start, angle_end)
                
                x = r * np.cos(theta)
                y = r * np.sin(theta)
                
                intensity = np.random.uniform(0.2, 1.0)
                pixel_dot = Dot(
                    offset_right + np.array([x, y, 0]),
                    radius=0.06,
                    color=interpolate_color(BLUE_E, YELLOW, intensity)
                )
                pixels_polar.add(pixel_dot)
        
        self.play(FadeIn(pixels_polar, lag_ratio=0.02), run_time=2)
        self.wait(2.5)  # NARRATION: "On the right: pixels naturally organize into angular bins"
        
        # ===== PART 5: Averaging/Binning =====
        self.play(FadeOut(subtitle4), run_time=0.5)
        subtitle5 = Text("Averaging: Different Intensities per Bin", font_size=26, color=GREEN)
        subtitle5.next_to(title, DOWN, buff=0.2)
        self.play(Write(subtitle5), run_time=1)
        
        # Fade out the left side (Cartesian) completely
        self.play(
            FadeOut(left_label),
            FadeOut(cart_grid_left),
            FadeOut(pixels_cart_left),
            FadeOut(strip_outer_left),
            FadeOut(strip_inner_left),
            FadeOut(strip_fill_left),
            run_time=1
        )
        
        # Move polar grid to the MIDDLE
        offset_middle = ORIGIN + DOWN * 0.3
        move_vector = offset_middle - offset_right
        
        self.play(
            right_label.animate.shift(move_vector),
            polar_grid_right.animate.shift(move_vector),
            strip_inner_right.animate.shift(move_vector),
            strip_outer_right.animate.shift(move_vector),
            strip_fill_right.animate.shift(move_vector),
            pixels_polar.animate.shift(move_vector),
            run_time=1.5
        )
        self.wait(1)
        
        # Animate averaging - KEEP DOTS STATIONARY IN THE STRIP
        averaged_dots = VGroup()
        
        strip_r_avg = (strip_r_min + strip_r_max) / 2
        
        # Store intensities for each bin to create variation
        np.random.seed(42)
        bin_intensities = np.random.uniform(0.3, 0.95, n_angle_bins)
        
        for i in range(n_angle_bins):
            angle_start = i * 2 * np.pi / n_angle_bins
            angle_end = (i + 1) * 2 * np.pi / n_angle_bins
            angle_center = (angle_start + angle_end) / 2
            
            # Find pixels in this angular bin
            bin_pixels = []
            for pixel in pixels_polar:
                px, py = (pixel.get_center() - offset_middle)[:2]
                pixel_angle = np.arctan2(py, px)
                if pixel_angle < 0:
                    pixel_angle += 2 * np.pi
                
                # Check if pixel is in this angular bin
                if angle_start <= pixel_angle < angle_end:
                    bin_pixels.append(pixel)
            
            if bin_pixels:
                # Use the pre-generated intensity for this bin
                avg_intensity = bin_intensities[i]
                
                # Color based on intensity
                avg_color = interpolate_color(BLUE_E, YELLOW, avg_intensity)
                
                # Size based on intensity
                avg_radius = 0.1 + 0.08 * avg_intensity
                
                # Position IN THE STRIP at the center of the angular bin
                x_avg = strip_r_avg * np.cos(angle_center)
                y_avg = strip_r_avg * np.sin(angle_center)
                
                avg_dot = Dot(
                    offset_middle + np.array([x_avg, y_avg, 0]),
                    radius=avg_radius,
                    color=avg_color,
                    stroke_width=2,
                    stroke_color=WHITE
                )
                averaged_dots.add(avg_dot)
        
        # Fade the original pixels and show the averaged ones
        # NO SCALING OR MOVEMENT - just fade in and keep stationary
        self.play(
            pixels_polar.animate.set_opacity(0.2),
            run_time=1
        )
        self.play(FadeIn(averaged_dots, lag_ratio=0.05), run_time=2)
        self.wait(2.5)  # NARRATION: "Each bin gets a different average - notice the varying sizes and colors"
        
        # Keep dots stationary - just fade out the faded pixels
        self.play(
            FadeOut(pixels_polar),
            run_time=0.8
        )
        self.wait(2)  # NARRATION: "This variation represents the actual finger pattern"
        
        # Show binned_statistic code
        # IMPORTANT: Fade out right_label (Polar Solution title) with the polar figure
        self.play(
            FadeOut(right_label),  # Title vanishes with the figure
            FadeOut(polar_grid_right),
            FadeOut(strip_inner_right),
            FadeOut(strip_outer_right),
            FadeOut(strip_fill_right),
            FadeOut(averaged_dots),
            FadeOut(subtitle5),
            run_time=1
        )
        
        code_title = Text("Python Implementation: Binning", font_size=32, color=BLUE)
        code_title.next_to(title, DOWN, buff=0.5)
        self.play(Write(code_title), run_time=1)
        
        binning_code_text = """from scipy import stats

bin_means, bin_edges, _ = stats.binned_statistic(
    theta_strip,
    intensity_strip,
    statistic='mean',
    bins=n_bins,
    range=(0, 360)
)"""
        
        binning_code = Code(
            code_string=binning_code_text,
            language="python",
            tab_width=4,
            background="window",
            formatter_style="monokai"
        ).scale(0.7).shift(DOWN * 0.8)
        
        self.play(FadeIn(binning_code, shift=UP), run_time=1.5)
        self.wait(3)  # NARRATION: "Using scipy's binned_statistic to compute the mean intensity per angular bin"
        
        # Final fade
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=1)
