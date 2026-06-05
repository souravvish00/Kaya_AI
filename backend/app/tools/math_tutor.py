from __future__ import annotations

import math
import re


def looks_like_grade_12_math(message: str) -> bool:
    lowered = message.lower()
    keywords = (
        "derivative",
        "differentiate",
        "integration",
        "integrate",
        "quadratic",
        "matrix",
        "determinant",
        "vector",
        "probability",
        "binomial",
        "ap",
        "gp",
        "sequence",
        "trigonometry",
        "limit",
        "12th",
        "class 12",
        "grade 12",
    )
    return any(keyword in lowered for keyword in keywords)


def answer_grade_12_math(message: str) -> dict:
    lowered = message.lower()

    quadratic = _solve_quadratic(message)
    if quadratic:
        return _ok(quadratic)

    derivative = _differentiate_polynomial(message)
    if derivative:
        return _ok(derivative)

    integral = _integrate_polynomial(message)
    if integral:
        return _ok(integral)

    if "ap" in lowered or "arithmetic progression" in lowered:
        return _ok(
            "Arithmetic progression guide:\n"
            "1. nth term: a_n = a + (n - 1)d\n"
            "2. Sum of first n terms: S_n = n/2 [2a + (n - 1)d]\n"
            "3. If two terms are known, subtract their equations to find d, then find a.\n"
            "Example: if a = 3, d = 5, n = 10, then a_10 = 3 + 9(5) = 48."
        )

    if "gp" in lowered or "geometric progression" in lowered:
        return _ok(
            "Geometric progression guide:\n"
            "1. nth term: a_n = ar^(n - 1)\n"
            "2. Sum when r != 1: S_n = a(r^n - 1)/(r - 1)\n"
            "3. Infinite sum exists only when |r| < 1, and S_infinity = a/(1 - r)."
        )

    if "matrix" in lowered or "determinant" in lowered:
        return _ok(
            "Matrix and determinant guide:\n"
            "1. For a 2x2 matrix [[a, b], [c, d]], determinant = ad - bc.\n"
            "2. Inverse exists only if determinant is not zero.\n"
            "3. A^-1 = 1/(ad - bc) [[d, -b], [-c, a]]."
        )

    if "vector" in lowered:
        return _ok(
            "Vector guide:\n"
            "1. Dot product: a.b = |a||b|cos(theta).\n"
            "2. For a = (a1, a2, a3), b = (b1, b2, b3), a.b = a1b1 + a2b2 + a3b3.\n"
            "3. If a.b = 0, the vectors are perpendicular."
        )

    if "probability" in lowered:
        return _ok(
            "Probability guide:\n"
            "1. P(A) = favourable outcomes / total outcomes.\n"
            "2. P(A union B) = P(A) + P(B) - P(A intersection B).\n"
            "3. Conditional probability: P(A|B) = P(A intersection B) / P(B)."
        )

    return _ok(
        "For 12th-grade math, I can help with derivatives, integrals, quadratics, AP/GP, "
        "matrices, vectors, probability, and limits. Ask with the exact expression, for example: "
        "'differentiate 3x^3 - 2x^2 + 5x' or 'solve quadratic x^2 - 5x + 6 = 0'."
    )


def _solve_quadratic(message: str) -> str | None:
    expression = _extract_expression(message)
    if not expression:
        return None

    coefficients = _quadratic_coefficients(expression)
    if coefficients is None:
        return None

    a, b, c = coefficients
    if a == 0:
        return None

    discriminant = b * b - 4 * a * c
    if discriminant < 0:
        root_part = f"sqrt({abs(discriminant)})i"
        roots = f"({-b} +/- {root_part})/{2 * a}"
    else:
        sqrt_d = math.sqrt(discriminant)
        roots = f"x = {_format_number((-b + sqrt_d) / (2 * a))}, x = {_format_number((-b - sqrt_d) / (2 * a))}"

    return (
        f"Quadratic equation: {a}x^2 + {b}x + {c} = 0\n"
        f"1. Compare with ax^2 + bx + c = 0, so a = {a}, b = {b}, c = {c}.\n"
        f"2. Discriminant D = b^2 - 4ac = {discriminant}.\n"
        f"3. Use x = (-b +/- sqrt(D)) / 2a.\n"
        f"Answer: {roots}"
    )


def _differentiate_polynomial(message: str) -> str | None:
    if "differentiate" not in message.lower() and "derivative" not in message.lower():
        return None

    expression = _extract_expression(message)
    terms = _parse_polynomial(expression)
    if not terms:
        return None

    derivative_terms = []
    for power, coefficient in terms:
        if power == 0:
            continue
        derivative_terms.append((power - 1, coefficient * power))

    derivative = _format_polynomial(derivative_terms) or "0"
    return (
        f"Differentiate: {expression}\n"
        "Rule used: d/dx(ax^n) = anx^(n - 1), and constants become 0.\n"
        f"Answer: {derivative}"
    )


def _integrate_polynomial(message: str) -> str | None:
    if "integrate" not in message.lower() and "integration" not in message.lower():
        return None

    expression = _extract_expression(message)
    terms = _parse_polynomial(expression)
    if not terms:
        return None

    integrated_terms = [(power + 1, coefficient / (power + 1)) for power, coefficient in terms]
    integral = _format_polynomial(integrated_terms)
    return (
        f"Integrate: {expression}\n"
        "Rule used: integral of ax^n dx = ax^(n + 1)/(n + 1) + C, when n != -1.\n"
        f"Answer: {integral} + C"
    )


def _extract_expression(message: str) -> str:
    expression = message.lower()
    for word in ("differentiate", "derivative of", "integrate", "integration of", "solve quadratic", "solve"):
        expression = expression.replace(word, "")
    expression = expression.replace("= 0", "").replace("=0", "")
    return expression.strip(" :.")


def _quadratic_coefficients(expression: str) -> tuple[float, float, float] | None:
    terms = _parse_polynomial(expression)
    if not terms:
        return None

    values = {0: 0.0, 1: 0.0, 2: 0.0}
    for power, coefficient in terms:
        if power > 2:
            return None
        values[power] += coefficient
    return values[2], values[1], values[0]


def _parse_polynomial(expression: str) -> list[tuple[int, float]]:
    normalized = expression.replace(" ", "").replace("^", "**")
    normalized = normalized.replace("-", "+-")
    if normalized.startswith("+"):
        normalized = normalized[1:]

    terms = []
    for raw_term in normalized.split("+"):
        if not raw_term:
            continue
        match = re.fullmatch(r"([+-]?\d*\.?\d*)\*?x(?:\*\*(\d+))?", raw_term)
        if match:
            coefficient_text, power_text = match.groups()
            if coefficient_text in ("", "+"):
                coefficient = 1.0
            elif coefficient_text == "-":
                coefficient = -1.0
            else:
                coefficient = float(coefficient_text)
            terms.append((int(power_text or "1"), coefficient))
            continue

        constant_match = re.fullmatch(r"[+-]?\d+(\.\d+)?", raw_term)
        if constant_match:
            terms.append((0, float(raw_term)))
            continue

        return []

    return terms


def _format_polynomial(terms: list[tuple[int, float]]) -> str:
    parts = []
    for power, coefficient in terms:
        if abs(coefficient) < 1e-12:
            continue
        sign = "-" if coefficient < 0 else "+"
        absolute = abs(coefficient)
        number = "" if absolute == 1 and power != 0 else _format_number(absolute)
        if power == 0:
            body = number
        elif power == 1:
            body = f"{number}x"
        else:
            body = f"{number}x^{power}"
        parts.append((sign, body))

    if not parts:
        return "0"

    first_sign, first_body = parts[0]
    output = f"-{first_body}" if first_sign == "-" else first_body
    for sign, body in parts[1:]:
        output += f" {sign} {body}"
    return output


def _format_number(value: float) -> str:
    if abs(value - round(value)) < 1e-12:
        return str(int(round(value)))
    return f"{value:.6g}"


def _ok(response: str) -> dict:
    return {"ok": True, "response": response}
