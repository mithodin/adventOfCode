import {solve1, solve2} from "./solution.ts";

const input = Deno.readTextFileSync("./input.txt");

console.log(solve1(input));
console.log(solve2(input));
