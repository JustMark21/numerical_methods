> **Preface:** The last one or two rows of most tables have strange ratios, that's because the error has reached the limit of double precision, so the last errors are just rounding noise and the ratios are meaningless. I ignored those.

## Bisection Method:

The bisection method halves the interval on each iteration and looks where the functions have different signs to choose the next interval. It is slow but always works.

**Problem 1: beam deflection:**
It worked but slowly. This method required 36 iterations on the interval from 0 to 4 to find the correct root 2.2360679774. I used [0,4] instead of [0,L]=[0,5] because f(5)=0 too, but x=5 is the support of the beam, not the maximum deflection. On [0,5] the method would just return 5.

**Problem 2: Kepler's equation:**
Same here, bisection method is still slow. It required us to complete 35 iterations on the interval [0,π] to find the correct root.

I also checked the theoretical bound eₙ ≤ (b−a)/2ⁿ on every iteration and it held every time.

Bisection method is slow but reliable, it requires about the same number of iterations because the number of iterations depends only on the interval length and the tolerance, and the intervals [0,4] and [0,π] have similar lengths.

## False Position Method:

This method is like a joint of secant method with bisection method, it takes two points and draws a line and looks for the x intercept of that line, which is the descriptions of the secant method. After that, it looks where the signs are different to look for a new, smaller interval.

**Problem 1: beam deflection:** very good, it took just 5 iterations, success! The root is an inflection point, so the line crossed it from both sides and neither endpoint got stuck.

**Problem 2: Kepler's equation:** it played worse here, 17 iterations. The right endpoint stayed fixed the whole time because f(pn) was always negative. As theory predicts, we have a linear convergence here. Good enough.

As we may see, the false position is way faster than bisection method in both cases, but the speed is very dependent on the shape of the function.

## Newton Method:

This method takes the tangent line at our point and looks where it crosses zero. Its theoretical order of convergence is 2, which is quadratic. This method is fast but requires the derivative.

**Problem 1: beam deflection:** the best result, 4 iterations. Better than theory predicts, because f’’ = 0 at the root, so Newton converges even faster than quadratically. Deriving f’ was easy here because f is a polynomial.

**Problem 2: Kepler's equation:** very good, it took 5 iterations here, and the ratio eₙ/eₙ₋₁² came to 0.2604, which is absolutely matches the theory: f’’(p)/(2f’(p)) = 0.2604.

So far the Newton is the fastest in both problems. Its downside is that we need the derivative, and it could fail with a bad starting point.

## Secant Method:

The idea is similar to Newton, but instead of the derivative it uses the line through the last two points. No derivative needed. Its theoretical order of convergence is about 1.618, so it's slower than Newton but faster than linear.

**Problem 1: beam deflection:** good, 5 iterations from 1 and 3. That's just one more than Newton, without needing f’.

**Problem 2: Kepler's equation:** it was OK, 8 iterations starting from 0 and π. It was slower here mainly because the starting points were far apart. Its first step gives 1.25, exactly the same point as the first false position step, because the formula is the same. The difference is that secant always uses the last two points instead of looking where sign changes like false position does – it is the reason why secant's iterations are quicker.

The secant method is a good compromise, almost as fast as Newton without a derivative. It's sensitive to the starting points.

## Muller Method:

Fit a parabola through the last three points and take where it crosses zero. Its theoretical order is about 1.84, between secant and Newton. It can also find complex roots.

**Problem 1: beam deflection:** good, 5 iterations from 1, 2 and 3, the same as secant.

**Problem 2:** the best in iteration count, only 4 iterations from 0, 1 and 2, one fewer than Newton. There weren't enough iterations for the ratio column to settle clearly, so I wouldn't draw strong conclusions about the order from it.

This method is very fast, but each step does more work and it's the most complicated to implement. It needs three starting points.

## Best method for each problem:

**Problem 1:** Newton. It took just 4 iterations. The derivative is a simple polynomial, so f’ is easy to compute. The root being an inflection point made it converge even faster than usual. Secant got second place here.

**Problem 2:** Newton, even though Müller took one fewer iteration. Newton is simpler and the derivative is easy. It also matched the theory perfectly. Secant with 8 iterations have my second place. I wouldn't want to use Muller method even with 4 iterations, it is the most complicated to implement.

---

**Potential for improvement:** I would add a timer to each function to see how long each method actually takes to find the root, and add one more function to the class that runs all the methods several times and calculates the average time. I could also count how many times each method calls f, because Müller needs fewer iterations but does more work in each one.
