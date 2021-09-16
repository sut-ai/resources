# Resources

## Admin Guide

### Theoretical Homeworks

1. Use [this template](https://github.com/sut-ai/hw-template) to create a new repository for the homework. The name of the repository should follow the pattern of `<S (for Spring) or F (for Fall)><year>-T<homework-number>-P<part-number>`. For example `F2021-T1-P1`.

1. Push the questions and solutions to the repository. The PDF of the homework will be generated automatically to the `build` branch of that repository.

1. Release the homework using [this action](https://github.com/sut-ai/resources/actions/workflows/release-hw.yml).
    Inputs:

    - The repository name. (e.g. `F2021-T1-P1`)
    - PDF file to be released (MUST be built inside build branch)
    - Path to the target file (e.g. `problem_sets/rohban_f2021/theoretical/T1/T1P1_questions.pdf`)

