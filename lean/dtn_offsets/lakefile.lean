import Lake
open Lake DSL

/-!
Downstream project of LeanMaster (recipe (A) of `docs/USING_LEANMASTER.md`): reuses LeanMaster's built Mathlib on the
same machine. Only `import Mathlib` is used; nothing of LeanMaster's own libraries is imported.
Toolchain `leanprover/lean4:v4.34.0-rc2` must equal LeanMaster's.
-/

package «dtn-offsets» where
  packagesDir := "/mnt/disks/disk-socrateai-local-1/leanmaster/lake/packages"
  leanOptions := #[⟨`maxHeartbeats, (1000000 : Nat)⟩]

require «SocrateAI-Scientific-Agora-LeanMaster» from
  "/home/callensxavier_gmail_com/SocrateAI-Scientific-Agora-LeanMaster"

@[default_target]
lean_lib «DtNOffsets» where
  roots := #[`DtNOffsets, `GramSchmidtBound, `SSHWinding]
