# Functional Image Processing Assignment

## Overview

Implement a functional image processing pipeline that operates on BMP files using **generators**, **function composition**, and **manual currying**. Your implementation must support the usage patterns demonstrated in `usage_examples.py`.

## Learning Objectives

- Master Python generator functions and lazy evaluation
- Implement currying using nested functions and closures
- Practice function composition for building transformation pipelines
- Understand streaming data processing with constant memory usage

## Prohibited

**You MAY NOT use:**
- `functools.partial` or any currying utilities
- Any third-party libraries except PIL/Pillow (for GIF writing only)
- Lambda functions for implementing currying (use proper `def` statements)

**You MUST implement currying manually using nested functions.**

## Files to Implement

### 1. `bmp_reader.py`

Implement `read_bmp(filename)` - a generator that:
- Yields metadata dictionary first: `{'width': int, 'height': int, 'bit_depth': int}`
- Then yields rows as lists of RGB tuples: `[(R,G,B), (R,G,B), ...]`
- Supports 8-bit indexed and 24-bit RGB BMPs
- Uses helper functions from `bmp_reader_utils.py`

**Key requirement:** Must be a generator for lazy evaluation.

### 2. `bmp_writer.py`

Implement `write_bmp(bit_depth, filename)` - a curried writer that:
- Takes `bit_depth` (8 or 24) and `filename` as separate parameters
- Returns a function that consumes a row generator
- Streams 24-bit output row-by-row (low memory)
- Buffers 8-bit output for color quantization
- Uses helper functions from `bmp_writer_utils.py`

### 3. `gif_writer.py`

Implement `write_gif(filename)` that:
- Takes `filename` and returns a writer function that consumes a row generator
- Uses `gif_utils.py` helper functions

### 4. `transformations.py`

Implement these transformation generators:

**Simple transformers:**
- `flip_horizontal(row_generator)` - mirrors left-right
- `flip_vertical(row_generator)` - mirrors top-bottom (requires buffering)
- `grayscale(row_generator)` - converts to grayscale using luminance formula

**Curried transformer:**
- `brightness(factor)` - returns a function that adjusts brightness

**Key requirements:**
- Each must pass through metadata unchanged
- Each yields transformed rows
- Must be generators

### 5. `pipeline.py`

Implement:
- `execute_transformation_pipeline(input_generator, transformations, image_writer)` - applies transformations and writes output
- `compose(*functions)` - compose functions right-to-left (mathematical order)
- `pipe(*functions)` - compose functions left-to-right (more intuitive)

**Key requirement:** Both `compose` and `pipe` must return a single composed function that can be applied to data.

### 6. `pipeline_helpers.py`

Implement these currying helper functions using **manual currying**:

## Currying Requirements

**You MAY NOT use `functools.partial` or any currying utilities.**

Review the docstrings in the provided files for guidance on function signatures and usage patterns.

## Generator Protocol

All generators must:
1. Yield metadata dictionary first
2. Pass through metadata unchanged
3. Then yield transformed rows

Review the transformation function docstrings for the expected pattern.

## Testing Your Implementation

Run `usage_examples.py` - all 17 examples must work correctly:

```bash
python usage_examples.py
```

Each example demonstrates a required feature:
- Examples 1-11: Basic pipeline functionality
- Examples 12-17: Currying patterns and reusable components

## Grading Criteria

| Component | Points | Requirements |
|-----------|--------|-------------|
| BMP Reader | 20 | Correct generator, supports 8/24-bit, proper metadata |
| BMP Writer | 20 | Curried correctly, streams 24-bit, handles 8-bit quantization |
| GIF Writer | 10 | Curried correctly, works with helpers |
| Transformations | 25 | All transformers work, proper generators, brightness curried |
| Pipeline | 15 | Executes correctly, integrates transformations |
| Manual Currying | 10 | No `partial`, proper nested functions, clear closures |
| **Total** | **100** | |

## Notes

Review the comments in provided files - they contain detailed implementation guidance. For conceptual questions about currying and generators, see the course materials on functional programming.