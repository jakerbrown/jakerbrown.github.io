Fixed blog math rendering so TeX notation can display properly on the website.

Updated the blog generator to preserve inline and display math, added MathJax to the blog page template, added a little CSS for equation spacing and mobile overflow, and rebuilt the generated blog pages.

This mattered because the place-effects post contained lots of math notation, and the old renderer was escaping it as plain text instead of letting the browser typeset it.

Verified in the generated HTML that the blog now includes the MathJax loader, keeps inline TeX delimiters intact, and wraps display equations in dedicated math blocks. I did not visually test in a browser inside this session.
