"""
Example Usage of the Functional BMP Processing Pipeline

This script demonstrates various ways to use the functional BMP processing pipeline,
including simple flips, composed transformations, currying, and more complex workflows.
Each function demonstrates a different aspect of the pipeline's functionality,
which you are expected to support in your implementation of the pipeline.
Each example is designed to showcase a specific feature or pattern of usage,
"""

from bmp_reader import read_bmp
from bmp_writer import write_bmp
from gif_writer import write_gif
from transformations import (
    flip_horizontal, flip_vertical, 
    grayscale, brightness
)
from pipeline import compose, execute_transformation_pipeline, pipe
from pipeline_helpers import (
    make_writer, from_file, 
    from_file_with_transforms, with_transforms
)


def example1_simple_flip():
    """Example 1: Simple horizontal flip"""
    print("Example 1: Horizontal flip")
    
    # Read, transform, write
    input_gen = read_bmp("./input/input.bmp")
    transformed = flip_horizontal(input_gen)
    write_bmp(24, "./output/example1_flipped.bmp")(transformed)


def example2_composition():
    """Example 2: Compose multiple transformations"""
    print("Example 2: Composed transformations")
    
    # Create pipeline using compose (right-to-left)
    pipeline = compose(
        brightness(1.2),
        grayscale,
        flip_horizontal
    )
    
    # Apply pipeline
    transformed = pipeline(read_bmp("./input/input.bmp"))
    
    # Write as 8-bit grayscale
    write_bmp(8, "./output/example2_composed.bmp")(transformed)


def example3_currying():
    """Example 3: Demonstrate currying"""
    print("Example 3: Currying demonstration")
    
    # Partially apply write_bmp
    write_grayscale = write_bmp(8)
    write_rgb = write_bmp(24)
    
    # Use the curried functions
    input_gen = read_bmp("./input/input.bmp")
    transformed = grayscale(input_gen)
    write_grayscale("./output/example3_gray.bmp")(transformed)
    
    # Another example with brightness currying
    brighten = brightness(1.5)
    
    transformed = brighten(read_bmp("./input/input.bmp"))
    write_rgb("./output/example3_bright.bmp")(transformed)


def example4_pipe():
    """Example 4: Using pipe (left-to-right) instead of compose"""
    print("Example 4: Pipe transformations")
    
    # Pipe reads more naturally (left-to-right)
    pipeline = pipe(
        flip_horizontal,
        grayscale,
        brightness(1.2)
    )
    
    transformed = pipeline(read_bmp("./input/input.bmp"))
    write_bmp(8, "./output/example4_piped.bmp")(transformed)


def example5_inline():
    """Example 5: Inline composition"""
    print("Example 5: Inline composition")
    
    # Everything in one expression
    write_bmp(8, "./output/example5_inline.bmp")(
        compose(
            brightness(0.8),
            grayscale,
            flip_vertical
        )(read_bmp("./input/input.bmp"))
    )


def example6_complex_pipeline():
    """Example 6: Complex multi-stage pipeline"""
    print("Example 6: Complex pipeline")
    
    # Build a complex transformation
    pipeline = compose(
        brightness(1.2),        # Brighten
        grayscale,              # Convert to grayscale
        flip_horizontal,        # Flip horizontally
        flip_vertical           # Flip vertically
    )
    
    # Apply and write
    write_bmp(8, "./output/example6_complex.bmp")(
        pipeline(read_bmp("./input/input.bmp"))
    )


def example7_reusable_pipeline():
    """Example 7: Reusable pipeline components"""
    print("Example 7: Reusable pipelines")
    
    # Define reusable transformation pipelines
    artistic_effect = compose(
        brightness(1.2),
        grayscale
    )
    
    mirror_effect = compose(
        flip_vertical,
        flip_horizontal
    )
    
    # Combine pipelines
    full_pipeline = compose(
        artistic_effect,
        mirror_effect
    )
    
    # Apply to multiple images
    for i in range(1, 4):
        write_bmp(8, f"./output/example7_{i}.bmp")(
            full_pipeline(read_bmp(f"./input/input_{i}.bmp"))
        )


def example8_lazy_evaluation():
    """Example 8: Demonstrate lazy evaluation"""
    print("Example 8: Lazy evaluation demonstration")
    
    # None of these transformations execute yet
    pipeline = compose(
        brightness(1.2),
        grayscale,
        flip_horizontal
    )
    
    input_gen = read_bmp("./input/input.bmp")
    transformed = pipeline(input_gen)
    
    # Still no processing has occurred!
    # Processing happens only when write_bmp consumes the generator
    
    output_sink = write_bmp(8, "./output/example8_lazy.bmp")
    output_sink(transformed)  # NOW processing happens row-by-row


def example9_gif_output():
    """Example 9: Writing to GIF format"""
    print("Example 9: GIF output")
    
    # Same pipeline, different output format
    pipeline = compose(
        brightness(1.2),
        grayscale,
        flip_horizontal
    )
    
    # Write as GIF instead of BMP
    write_gif("./output/example9.gif")(
        pipeline(read_bmp("./input/input.bmp"))
    )


def example10_mixed_formats():
    """Example 10: Read BMP, write both BMP and GIF"""
    print("Example 10: Mixed output formats")
    
    # Create pipeline
    pipeline = compose(
        brightness(1.3),
        grayscale
    )
    
    # Note: We need to read twice since generators are consumed
    # Read and process twice
    write_bmp(8, "./output/example10.bmp")(pipeline(read_bmp("./input/input.bmp")))
    write_gif("./output/example10.gif")(pipeline(read_bmp("./input/input.bmp")))


def example11_gif_color_vs_grayscale():
    """Example 11: GIF with color vs grayscale"""
    print("Example 11: GIF color and grayscale")
    
    # Color GIF (will be quantized to 256 colors)
    write_gif("./output/example11_color.gif")(
        compose(
            brightness(1.1),
            flip_horizontal
        )(read_bmp("./input/input.bmp"))
    )
    
    # Grayscale GIF
    write_gif("./output/example11_gray.gif")(
        compose(
            grayscale,
            brightness(1.2)
        )(read_bmp("./input/input.bmp"))
    )


def example12_currying_pattern1():
    """Example 12: Pattern 1 - Lock input, vary transformations"""
    print("Example 12: Currying Pattern 1 - Lock input file")
    
    # Create reusable writers using manual currying
    bmp_8 = make_writer(write_bmp, 8)
    bmp_24 = make_writer(write_bmp, 24)
    gif_writer = write_gif
    
    # Lock the input file
    process_photo = from_file('./input/photo.bmp')
    
    # Apply different transformations to the same photo
    process_photo([flip_horizontal, grayscale], bmp_8('./output/example12_gray.bmp'))
    process_photo([brightness(1.5)], bmp_24('./output/example12_bright.bmp'))
    process_photo([brightness(0.7)], gif_writer('./output/example12_dark.gif'))
    process_photo([grayscale, brightness(0.8)], gif_writer('./output/example12_bw.gif'))


def example13_currying_pattern2():
    """Example 13: Pattern 2 - Lock input and transformations"""
    print("Example 13: Currying Pattern 2 - Lock input and transformations")
    
    # Lock input and transformations, save to different formats
    photo_to_grayscale = from_file_with_transforms('./input/photo.bmp', [grayscale])
    
    photo_to_grayscale(write_bmp(8, './output/example13_gray_8bit.bmp'))
    photo_to_grayscale(write_bmp(24, './output/example13_gray_24bit.bmp'))
    photo_to_grayscale(write_gif('./output/example13_gray.gif'))


def example14_currying_pattern3():
    """Example 14: Pattern 3 - Lock transformations, batch process"""
    print("Example 14: Currying Pattern 3 - Batch processing")
    
    # Create reusable writers using manual currying
    bmp_8 = make_writer(write_bmp, 8)
    gif_writer = write_gif
    
    # Create a transformation to apply to multiple images
    make_artistic = with_transforms([grayscale, brightness(1.3)])
    
    # Apply to multiple photos
    make_artistic('./input/photo1.bmp', bmp_8('./output/example14_photo1_artistic.bmp'))
    make_artistic('./input/photo2.bmp', bmp_8('./output/example14_photo2_artistic.bmp'))
    make_artistic('./input/photo3.bmp', gif_writer('./output/example14_photo3_artistic.gif'))


def example15_reusable_writers():
    """Example 15: Creating reusable writer factories"""
    print("Example 15: Reusable writer factories")
    
    # Create reusable writer factories using manual currying
    bmp_8 = make_writer(write_bmp, 8)
    bmp_24 = make_writer(write_bmp, 24)
    gif_writer = write_gif
    
    # Use them in transformations
    process_photo = from_file('./input/photo.bmp')
    process_photo([grayscale], bmp_8('./output/example15_gray.bmp'))
    process_photo([brightness(1.2)], bmp_24('./output/example15_bright.bmp'))
    process_photo([brightness(0.6)], gif_writer('./output/example15_dark.gif'))


def example16_complete_workflow():
    """Example 16: Complete real-world workflow"""
    print("Example 16: Complete workflow")
    
    # Setup: Create reusable writers using manual currying
    bmp_8 = make_writer(write_bmp, 8)
    bmp_24 = make_writer(write_bmp, 24)
    gif_writer = write_gif
    
    # Step 1: Experiment with one photo
    print("  Experimenting with transformations...")
    experiment = from_file('./input/test_photo.bmp')
    experiment([grayscale], bmp_8('./output/example16_test_gray.bmp'))
    experiment([brightness(1.2)], bmp_24('./output/example16_test_bright.bmp'))
    experiment([flip_horizontal, brightness(1.2)], bmp_24('./output/example16_test_flipped_bright.bmp'))
    
    # Step 2: Apply chosen effect to all photos
    print("  Applying enhancement to batch...")
    enhance_photos = with_transforms([brightness(1.2), flip_vertical])
    for i in range(1, 4):
        enhance_photos(f'./input/photo_{i}.bmp', bmp_24(f'./output/example16_enhanced_{i}.bmp'))
    
    # Step 3: Create web thumbnails
    print("  Creating thumbnails...")
    create_thumbnail = with_transforms([grayscale, brightness(0.8)])
    for i in range(1, 4):
        create_thumbnail(f'./input/photo_{i}.bmp', gif_writer(f'./output/example16_thumb_{i}.gif'))
    
    # Step 4: Multi-format export
    print("  Exporting to multiple formats...")
    hero_flipped = from_file_with_transforms('./input/hero_photo.bmp', [flip_horizontal])
    hero_flipped(bmp_24('./output/example16_hero_flipped.bmp'))
    hero_flipped(bmp_8('./output/example16_hero_flipped_compressed.bmp'))
    hero_flipped(gif_writer('./output/example16_hero_flipped.gif'))


def example17_direct_transform_image():
    """Example 17: Using execute_transformation_pipeline directly"""
    print("Example 17: Direct transform_image usage")
    
    # Direct usage without helper functions
    execute_transformation_pipeline(
        read_bmp('./input/input.bmp'),
        [flip_horizontal, grayscale],
        write_bmp(8, './output/example17.bmp')
    )
    
    # Manual currying for custom patterns
    def process_photo(transformations, output_writer):
        """Manually curried function with './input/photo.bmp' baked in."""
        execute_transformation_pipeline(read_bmp('./input/photo.bmp'), transformations, output_writer)
    
    process_photo([brightness(1.5)], write_bmp(24, './output/example17_bright.bmp'))
    process_photo([grayscale], write_gif('./output/example17_gray.gif'))


if __name__ == "__main__":
    # Run examples
    # Note: You'll need to provide input.bmp files for these to work
    
    # Make the ./output directory if it doesn't exist
    import os
    os.makedirs('./output', exist_ok=True)
    
    print("Functional BMP Processing Examples")
    print("=" * 50)
    
    example1_simple_flip()
    example2_composition()
    example3_currying()
    example4_pipe()
    example5_inline()
    example6_complex_pipeline()
    example7_reusable_pipeline()
    example8_lazy_evaluation()
    example9_gif_output()
    example10_mixed_formats()
    example11_gif_color_vs_grayscale()
    
    # New currying pattern examples
    example12_currying_pattern1()
    example13_currying_pattern2()
    example14_currying_pattern3()
    example15_reusable_writers()
    example16_complete_workflow()
    example17_direct_transform_image()
    
    print("\nExamples complete!")
