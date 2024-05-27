(define-private (tally (member principal) (accumulator uint))
	(if (get-vote member tx-sender) (+ accumulator u1) accumulator)
)

(define-read-only (tally-votes-fold)
	(fold tally (var-get members) u0)
)

(define-read-only (tally-votes-filter)
	(filter tally (var-get members) u0)
)

(define-read-only (tally-votes-map)
	(map tally (var-get members) u0)
)


(define-private (this_is_not_used (member principal) (accumulator uint))
	(if (get-vote member tx-sender) (+ accumulator u1) accumulator)
)


(define-public (withdraw)
	(let
		(
			(recipient tx-sender)
			(total-votes (tally-votes))
		)
		(asserts! (>= total-votes (var-get votes-required)) err-votes-required-not-met)
		(try! (as-contract (stx-transfer? (stx-get-balance tx-sender) tx-sender recipient)))
		(tally tx-sender 1)
		(ok total-votes)
	)
)

