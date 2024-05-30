
(define-public (some-function (another-contract principal) (param-A uint) (param-B uint))
	;; Keep in mind that another-contract will have the current contract as its tx-sender
	;; and the original tx-sender will be lost.
	(try! (as-contract (contract-call? another-contract param-A param-B)))
)