# Artificial Gravity: Why You Feel "Weight" in a Spinning Cylinder

## 1. The Setup

You're standing on the inner surface of a rotating cylinder in space. There is no gravitational pull worth mentioning — the cylinder's mass is far too small to produce meaningful gravity. The only real force on your body is the **floor pushing your feet inward**, toward the axis of rotation.

That's it. One force. Inward.

---

## 2. The Inertial (Outside) View

An observer floating outside the cylinder, not rotating, sees the following:

- You would naturally travel in a **straight line** (Newton's first law).
- The floor keeps shoving you inward, **bending your straight-line path into a circle**.
- That inward push is the centripetal force.

Applying Newton's second law to this situation:

$$
F = ma
$$

The force is the normal force $N$ from the floor (the only real force). The acceleration is centripetal, directed inward:

$$
a_c = \omega^2 r
$$

So:

$$
N = m \cdot \omega^2 r
$$

There is **no outward force** in this picture. The floor pushes in, you accelerate inward, Newton is satisfied.

---

## 3. Why You Feel "Gravity" Pulling You Outward

Here's the critical insight: **you don't feel acceleration. You feel forces acting on your body.**

On Earth, this is what happens:

- Gravity pulls you **down** (toward Earth's center).
- The ground pushes you **up** (normal force on your feet).
- You feel the ground pressing against your feet. You call this "weight."

In the spinning cylinder:

- The floor pushes you **inward** (toward the cylinder's axis).
- Nothing pulls you outward.
- But you feel the floor pressing against your feet — **exactly the same sensation**.

Your body has no way to distinguish between:

> "Gravity pulls me down and the floor stops me"

and

> "The floor pushes me inward to keep me on a circular path."

Both produce the same experience: pressure on the soles of your feet, objects falling when released (they stop co-rotating and drift to the floor), a sense of "down" being away from the axis.

**You feel pushed outward for the same reason you feel pushed into your car seat when accelerating forward — it's not that something pushes you backward, it's that the car pushes you forward and your inertia resists.** In the cylinder, the floor pushes you inward and your inertia wants to go straight. You interpret this resistance as "gravity pulling me outward."

---

## 4. The Fictitious Centrifugal Force

If you insist on doing physics **from inside the rotating frame** — treating the cylinder floor as stationary ground — Newton's laws break. You're standing still (in your frame), so $\vec{a} = 0$, but there's a real force $N$ pushing up on your feet. The math doesn't balance:

$$
N = ma = m \cdot 0 = 0 \quad \text{???}
$$

That's wrong — $N$ is clearly not zero. To fix this, you **invent a fictitious outward force** called the centrifugal force:

$$
F_{\text{centrifugal}} = m \cdot \omega^2 r \quad (\text{directed outward})
$$

Now in the rotating frame:

$$
N - F_{\text{centrifugal}} = 0 \quad \Longrightarrow \quad N = m\omega^2 r
$$

The normal force balances the centrifugal force, you're in equilibrium, and the math works again.

**But the centrifugal force is not real.** It's a mathematical correction you bolt on to make Newton's laws work in a non-inertial (rotating) reference frame. From the outside, it doesn't exist. From the inside, it's indistinguishable from gravity.

| Frame              | What you say                                               | Forces involved                      |
|--------------------|------------------------------------------------------------|--------------------------------------|
| Inertial (outside) | "The floor pushes her inward; she accelerates inward."     | Real: $N$ inward. That's all.        |
| Rotating (inside)  | "She's stationary; gravity pulls her down, floor holds her up." | Real: $N$ inward. Fictitious: $F_{\text{cf}}$ outward. |

Both frames give the same prediction for $N = m\omega^2 r$. They just explain it differently.

---

## 5. The $F = ma$ Substitution — Step by Step

Starting from first principles:

**Step 1 — Newton's second law:**

$$
F = ma
$$

**Step 2 — Identify the force:**

The floor exerts a normal force $N$ on you, directed radially inward (toward the axis). This is the only real force.

$$
N = ma
$$

**Step 3 — Identify the acceleration:**

You're moving in a circle, so the acceleration is centripetal:

$$
a = \omega^2 r
$$

**Step 4 — Substitute:**

$$
N = m \cdot \omega^2 r
$$

**Step 5 — Set equal to Earth gravity:**

For the normal force to feel like standing on Earth, we need $N = mg$, which means:

$$
m \cdot \omega^2 r = m \cdot g
$$

Cancel $m$:

$$
\omega^2 r = g
$$

**Step 6 — Solve for the design parameters:**

$$
\omega = \sqrt{\frac{g}{r}} \qquad \text{or} \qquad r = \frac{g}{\omega^2}
$$

That's the complete chain. $F = ma$ → identify force as $N$ → identify acceleration as $\omega^2 r$ → set equal to $g$ → solve for spin rate or radius.

---

## 6. Q&A

### Q: If centripetal acceleration is inward, why do I feel pushed outward?

You don't, strictly speaking. What you feel is the floor **pushing you inward**. Your body interprets that floor pressure as "something is pulling me into the floor" — just like on Earth. There is no outward force in the inertial frame. Your sense of "outward pull" is your inertia resisting the inward push, the same way you feel "pushed back" into your seat when a car accelerates forward.

### Q: Is the centrifugal force real?

**No.** It is a fictitious (pseudo) force that only appears when you do physics in a rotating reference frame. It exists as a mathematical tool to make $F = ma$ balance in a non-inertial frame. In the inertial frame, it doesn't exist — everything is explained by the real inward normal force.

That said, "fictitious" doesn't mean "irrelevant." If you live in the cylinder, the rotating frame is your everyday reality. In your daily experience, centrifugal force behaves exactly like gravity. You can use it in calculations, engineer with it, live your life by it. It's just not a fundamental force — it's a consequence of your reference frame.

### Q: What is the floor actually doing, physically?

The floor is a rigid surface moving in a circle. At every instant, your body wants to continue in a straight line (Newton's first law). The floor intercepts that straight line and pushes you inward, redirecting you into circular motion. This continuous inward push is what you experience as weight.

If the floor suddenly disappeared, you would not fly outward. You would fly off **tangentially** — in a straight line, in whatever direction you were moving at that instant. This is another clue that there's no outward force: remove the floor and nothing pushes you outward.

### Q: Is this the same as what happens in a car turning a corner?

Exactly. When a car turns left:

- The real force: the seat and seatbelt push you **left** (inward, toward the center of the turn).
- What you feel: pushed to the **right** (outward).
- What's actually happening: your body wants to go straight; the car pushes you into a curve. Your inertia resists.

The spinning cylinder is this, continuously, at every point, for every moment.

### Q: On Earth, gravity is a real downward force and the floor provides a real upward force. In the cylinder, the floor provides a real inward force — but what provides the "downward" (outward) force?

**Nothing.** That's the key difference. On Earth, there are two real forces: gravity down, normal force up. In the cylinder, there is only one real force: normal force inward. The "outward pull" you feel is fictitious — it's your inertia, not a force.

But the subjective experience is identical. Your body's internal sensors (the vestibular system, pressure on your feet, the way your blood pools) respond to the normal force, not to what's causing it. One real inward force produces the same sensation as a real downward pull opposed by a real upward push. Your body cannot tell the difference.

### Q: Why can we just "set $\omega^2 r = g$"? What justifies that substitution?

Because the **only thing your body measures** is the normal force on your feet. On Earth, that force is $N = mg$. In the cylinder, that force is $N = m\omega^2 r$. If you want them to feel the same:

$$
m\omega^2 r = mg \quad \Longrightarrow \quad \omega^2 r = g
$$

This isn't a deep physical equivalence (general relativity has more to say about that). It's an engineering condition: make the floor push on you with the same force that Earth's surface does, and you won't be able to feel the difference.
