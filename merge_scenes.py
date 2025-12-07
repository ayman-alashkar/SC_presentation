#!/usr/bin/env python3
"""
Merge all scene videos into a complete presentation
Alternative to FFmpeg method - uses moviepy
"""

from moviepy.editor import VideoFileClip, concatenate_videoclips
import os

def merge_presentation(quality='1080p60'):
    """
    Merge all scene videos into one complete presentation
    
    Args:
        quality: Video quality folder ('480p15', '720p30', or '1080p60')
    """
    
    # Define scene paths
    scenes = [
        f"media/videos/scene1/{quality}/IntroSceneWithTitles.mp4",
        f"media/videos/scene2/{quality}/CircleDetectionScene.mp4",
        f"media/videos/scene3/{quality}/PolarTransformScene.mp4",
        f"media/videos/scene4/{quality}/ResultsScene.mp4"
    ]
    
    # Check if all files exist
    print("Checking scene files...")
    missing = []
    for scene in scenes:
        if not os.path.exists(scene):
            missing.append(scene)
            print(f"  ❌ Missing: {scene}")
        else:
            print(f"  ✓ Found: {scene}")
    
    if missing:
        print(f"\n⚠️  {len(missing)} file(s) missing!")
        print("Please render all scenes first using:")
        print(f"  manim -pqh scenes/scene1.py IntroSceneWithTitles")
        print(f"  manim -pqh scenes/scene2.py CircleDetectionScene")
        print(f"  manim -pqh scenes/scene3.py PolarTransformScene")
        print(f"  manim -pqh scenes/scene4.py ResultsScene")
        return
    
    # Load video clips
    print("\nLoading video clips...")
    clips = []
    for i, scene in enumerate(scenes, 1):
        print(f"  Loading scene {i}/4...")
        clip = VideoFileClip(scene)
        clips.append(clip)
        print(f"    Duration: {clip.duration:.2f}s")
    
    # Concatenate clips
    print("\nMerging videos...")
    final_clip = concatenate_videoclips(clips, method="compose")
    
    total_duration = sum(clip.duration for clip in clips)
    print(f"  Total duration: {total_duration:.2f}s ({total_duration/60:.2f} minutes)")
    
    # Export
    output_file = "COMPLETE_PRESENTATION.mp4"
    print(f"\nExporting to {output_file}...")
    
    fps = 60 if '60' in quality else (30 if '30' in quality else 15)
    
    final_clip.write_videofile(
        output_file,
        fps=fps,
        codec='libx264',
        audio_codec='aac',
        temp_audiofile='temp-audio.m4a',
        remove_temp=True,
        preset='medium',
        threads=4
    )
    
    print(f"\n✅ Success! Complete presentation saved as: {output_file}")
    print(f"   File size: {os.path.getsize(output_file) / (1024*1024):.2f} MB")
    
    # Clean up
    for clip in clips:
        clip.close()
    final_clip.close()

if __name__ == "__main__":
    import sys
    
    # Check if quality argument provided
    if len(sys.argv) > 1:
        quality = sys.argv[1]
    else:
        quality = '1080p60'  # Default to high quality
    
    print("="*70)
    print("  MANIM PRESENTATION MERGER")
    print("="*70)
    print(f"\nQuality: {quality}")
    print("-"*70)
    
    merge_presentation(quality)
    
    print("\n" + "="*70)
    print("  Done!")
    print("="*70)
