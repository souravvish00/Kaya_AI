GRADE_12_MATH_EXAMPLES = [
    {
        "prompt": "Differentiate 3x^3 - 2x^2 + 5x - 7",
        "completion": (
            "Use d/dx(ax^n) = anx^(n-1). d/dx(3x^3)=9x^2, "
            "d/dx(-2x^2)=-4x, d/dx(5x)=5, and d/dx(-7)=0. "
            "Answer: 9x^2 - 4x + 5."
        ),
        "tags": ["math", "grade-12", "calculus", "derivative"],
        "rating": 5,
    },
    {
        "prompt": "Integrate 4x^3 - 6x + 2",
        "completion": (
            "Use integral ax^n dx = ax^(n+1)/(n+1) + C. "
            "Integral of 4x^3 is x^4, integral of -6x is -3x^2, "
            "and integral of 2 is 2x. Answer: x^4 - 3x^2 + 2x + C."
        ),
        "tags": ["math", "grade-12", "calculus", "integration"],
        "rating": 5,
    },
    {
        "prompt": "Solve quadratic x^2 - 5x + 6 = 0",
        "completion": (
            "Compare with ax^2 + bx + c = 0: a=1, b=-5, c=6. "
            "Discriminant D=b^2-4ac=25-24=1. "
            "x=(5 +/- 1)/2, so x=3 or x=2."
        ),
        "tags": ["math", "grade-12", "quadratic"],
        "rating": 5,
    },
    {
        "prompt": "Explain arithmetic progression formula for class 12",
        "completion": (
            "In an arithmetic progression, each term differs by common difference d. "
            "nth term: a_n = a + (n - 1)d. "
            "Sum: S_n = n/2 [2a + (n - 1)d]."
        ),
        "tags": ["math", "grade-12", "sequence", "ap"],
        "rating": 5,
    },
    {
        "prompt": "Explain dot product of vectors",
        "completion": (
            "For vectors a and b, a.b = |a||b|cos(theta). "
            "In coordinates, a.b = a1b1 + a2b2 + a3b3. "
            "If a.b = 0, the vectors are perpendicular."
        ),
        "tags": ["math", "grade-12", "vectors"],
        "rating": 5,
    },
    {
        "prompt": "Explain conditional probability",
        "completion": (
            "Conditional probability means probability of A when B has already happened. "
            "Formula: P(A|B) = P(A intersection B) / P(B), where P(B) is not zero."
        ),
        "tags": ["math", "grade-12", "probability"],
        "rating": 5,
    },
]
