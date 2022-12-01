import { assertEquals, assertArrayIncludes } from 'https://deno.land/std/testing/asserts.ts'
import {getTopN, parse, solve1, solve2} from "./solution.ts";

const test_input = `1000
2000
3000

4000

5000
6000

7000
8000
9000

10000`;

Deno.test("test example solution", () => {
    const solution = solve1(test_input);
    assertEquals(solution, 24000);
});

Deno.test("test part 2 example solution", () => {
    const solution = solve2(test_input);
    assertEquals(solution, 45000);
});

Deno.test("getTopN returns the highest number", () => {
    const solution = getTopN([1, 2, 3], 1);

    assertEquals(solution.length, 1);
    assertArrayIncludes(solution, [3]);
});


Deno.test("getTopN returns the highest two numbers", () => {
    const solution = getTopN([1, 2, 3], 2);

    assertEquals(solution.length, 2);
    assertArrayIncludes(solution, [2,3]);
});

Deno.test("getTopN returns the highest three numbers", () => {
    const solution = getTopN([5, 7, 1, 2, 3], 3);

    assertEquals(solution.length, 3);
    assertArrayIncludes(solution, [7, 5, 3]);
});

Deno.test("parser creates an array of arrays holding individual calorie counts", () => {
    const result = parse(test_input);
    assertArrayIncludes(result, [[1000, 2000, 3000], [4000], [5000,6000], [7000,8000,9000], [10000]]);
});
