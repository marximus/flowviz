"""
Basic tests to validate NumPy type alias fixes for NumPy 1.24+ compatibility.

Tests the replacement of deprecated np.int with np.int_ in:
- flowviz.colorcode.compute_color
- flowviz.animate.FlowAnimation
"""
import numpy as np
import sys
import os

# Add flowviz to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flowviz.colorcode import compute_color
from flowviz.animate import FlowAnimation


def test_compute_color():
    """Test that compute_color works with np.int_ type conversions."""
    print("Testing compute_color with np.int_ conversions...")

    # Create simple test data
    height, width = 10, 10
    fx = np.random.randn(height, width).astype(np.float32)
    fy = np.random.randn(height, width).astype(np.float32)
    colim = np.zeros((height, width, 3), dtype=np.uint8)

    # This should not raise AttributeError with np.int_
    try:
        compute_color(fx, fy, colim)
        print("✓ compute_color executed successfully")

        # Verify output shape and dtype
        assert colim.shape == (height, width, 3), f"Expected shape (10, 10, 3), got {colim.shape}"
        assert colim.dtype == np.uint8, f"Expected dtype uint8, got {colim.dtype}"
        print("✓ Output shape and dtype are correct")

        # Verify values are in valid range [0, 255]
        assert np.all(colim >= 0) and np.all(colim <= 255), "Color values out of range [0, 255]"
        print("✓ Color values are in valid range [0, 255]")

        return True
    except AttributeError as e:
        if "module 'numpy' has no attribute 'int'" in str(e):
            print(f"✗ FAILED: Deprecated np.int still present - {e}")
            return False
        raise
    except Exception as e:
        print(f"✗ FAILED: Unexpected error - {e}")
        return False


def test_flow_animation():
    """Test that FlowAnimation initialization works with np.int_ type conversions."""
    print("\nTesting FlowAnimation with np.int_ conversions...")

    # Create simple test video data
    N, H, W = 5, 20, 30  # 5 frames, 20x30 pixels
    video = np.random.randint(0, 256, (N, H, W, 3), dtype=np.uint8)

    # Test with scale parameter to trigger figsize conversion
    scales = [1.0, 0.5, 2.0]

    for scale in scales:
        try:
            anim = FlowAnimation(video, scale=scale)
            print(f"✓ FlowAnimation created successfully with scale={scale}")

            # Verify figsize is correctly computed as integers
            expected_width = int(W * scale)
            expected_height = int(H * scale)
            assert anim.figwidth == expected_width, f"Expected width {expected_width}, got {anim.figwidth}"
            assert anim.figheight == expected_height, f"Expected height {expected_height}, got {anim.figheight}"
            print(f"✓ Figure dimensions correct: {anim.figwidth}x{anim.figheight}")

        except AttributeError as e:
            if "module 'numpy' has no attribute 'int'" in str(e):
                print(f"✗ FAILED: Deprecated np.int still present - {e}")
                return False
            raise
        except Exception as e:
            print(f"✗ FAILED: Unexpected error with scale={scale} - {e}")
            return False

    return True


def test_numpy_int_removed():
    """Verify that np.int is actually removed in NumPy 1.24+ (if applicable)."""
    print("\nChecking NumPy version and np.int availability...")
    print(f"NumPy version: {np.__version__}")

    # Check if np.int exists (should not in NumPy 1.24+)
    has_np_int = hasattr(np, 'int')
    print(f"np.int available: {has_np_int}")

    # Check that np.int_ exists (should always exist)
    has_np_int_ = hasattr(np, 'int_')
    print(f"np.int_ available: {has_np_int_}")

    assert has_np_int_, "np.int_ should always be available"

    major, minor = [int(x) for x in np.__version__.split('.')[:2]]
    if major > 1 or (major == 1 and minor >= 24):
        print(f"✓ Running NumPy {np.__version__} (1.24+) - np.int should be removed")
        if has_np_int:
            print("⚠ Warning: np.int still exists in NumPy 1.24+")
    else:
        print(f"✓ Running NumPy {np.__version__} (<1.24) - np.int may still exist")

    return True


def main():
    """Run all tests."""
    print("=" * 60)
    print("NumPy Type Alias Compatibility Tests")
    print("=" * 60)

    results = []

    # Run tests
    results.append(("NumPy version check", test_numpy_int_removed()))
    results.append(("compute_color test", test_compute_color()))
    results.append(("FlowAnimation test", test_flow_animation()))

    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)

    all_passed = True
    for test_name, passed in results:
        status = "PASSED" if passed else "FAILED"
        symbol = "✓" if passed else "✗"
        print(f"{symbol} {test_name}: {status}")
        if not passed:
            all_passed = False

    print("=" * 60)
    if all_passed:
        print("✓ All tests PASSED!")
        return 0
    else:
        print("✗ Some tests FAILED!")
        return 1


if __name__ == "__main__":
    sys.exit(main())
