- **Full prologue loop deployed** (Title → Hotel → Tuktuk → BBQ → Victory → Replay) with localStorage save/restore, typewriter dialogue effect, item pickup toasts, and "New Game vs Continue" on title screen.

- **Contextual Action Labels added** — every interactive element now shows a tiny colored badge (Talk/Pick Up/Look/Use) so mobile players instantly know what a tap does without guessing.

- **Structured inventory system** — items are now `{ id, icon, label }` objects instead of plain strings, enabling future item combination/interaction mechanics. All scenes updated with `v-longpress` for mobile examine consistency.