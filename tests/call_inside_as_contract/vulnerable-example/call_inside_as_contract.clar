
(define-public (some-function (contract principal) (param-A uint) (param-B uint))
	(try! (as-contract (contract-call? contract param-A param-B)))
)