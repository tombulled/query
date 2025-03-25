from query.comparison_expressions import Eq, Gt, Gte, In, Lt, Lte, Ne, Nin

EXPRESSIONS = {
    Eq.operator: Eq.parse,
    Gt.operator: Gt.parse,
    Gte.operator: Gte.parse,
    In.operator: In.parse,
    Lt.operator: Lt.parse,
    Lte.operator: Lte.parse,
    Ne.operator: Ne.parse,
    Nin.operator: Nin.parse,
}

eq = Eq("name", "bob")
gt = Gt("age", 10)
gte = Gte("age", 10)
in_ = In("name", ("bob", "sally"))
lt = Lt("age", 10)
lte = Lte("age", 10)
ne = Ne("age", 10)
nin = Nin("age", (10, 20))
