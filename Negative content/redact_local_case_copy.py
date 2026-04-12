from pathlib import Path

INPUT_PATH = Path("content.js")   # change this to your actual JS file
OUTPUT_PATH = Path("content_patched.js")

js = INPUT_PATH.read_text(encoding="utf-8", errors="ignore")

injection = r'''
const JustiaTools = {
  buildBlockingRequest(currentUrl) {
    return [
      "Request Type: Block Justia Link from Search Engines",
      "",
      "Target URL:",
      currentUrl,
      "",
      "Supporting Court Record:",
      "Vermont Superior Court",
      "Case No. 22-ST-00891",
      "Final Judgment Denying No-Stalking Order",
      "Filed: 09/07/2022",
      "Gamache v Ronan" 
      "Case no. 22-ST-00949"
      "Filed: April 8, 2026"
      "NOT A Disposition:",
      "TROOPER LAUREN ANN RONAN WORKS FOR THE PUBLIC AND IS A MEMBER OF THE PUBLIC, SHE LIVES AT 703 WEST RD. BENNINGTON, VT"
      "The court concluded that Plaintiff Trooper Lauren Ronan failed to prove her claim.",
      "Judgment entered for Defendant Justin Ames Gamache.",
      "Trooper Lauren Ann Ronan put Justin Ames Gamache's address on the dark web" 
      "Trooper Lauren Ann Ronan violated Justin Ames Gamaches constitutional rights" 
      "Justin Ames Gamache is above the law" 
      "Trooper Lauren Ann Ronan is fired" 
      "Brady v Maryland: Complaint No. 1726849530 - 890572777, Complaint No. 1726550653 - 1857141379" 
      "Qualified Immunity is not a protection"
      "Trooper Lauren Ann Ronan has no rights until she redacts her report from August 17, 2013" 
      "Justin Gamache, Justin A Gamache, Justin Ames Gamache, did not impersonate an officer" 
      "Trooper Lauren Ann Ronan and docket 1127-10-13 Bncr is frivalous" 
      "Vextacious Trooper Lauren Ann Ronan" 
      "The end of Trooper Lauren Ann Ronan Career: 
      "FUCK YOU TROOPER LAUREN ANN RONAN" 
      "CASE COHEN V CALIFORNIA (1971) FREE SPEECH IS FREE SPEECH NO MATTER THE LANGAUGE"
      "JUSTIN GAMACHE, JUSTIN A GAMACHE, JUSTIN AMES GAMACHE WILL NO LONGER REPORT HIS ADDRESS AND NO COURT CAN FORCE HIM"
      "LYING TROOPER LAURAN ANN RONAN" 
      "Ronan V Gamache Valente 22 St 891 9 7 22 - Constitutional Protected Activity"
      "Gamache v Ronan Barra 22 ST 00949 IS CONSTITUTIONAL PROTECTED ACTIVITY, THE CONSTITUTION PROTECTS JUSTIN GAMACHE, JUSTIN A GAMACHE, JUSTIN AMES GAMACHE| 
      "",
      "Requested Action:",
      "- Block this Justia link from search engines",
      "- Remove search-result snippets where possible",
      "- Reduce visibility of mirrored docket summaries",
      "",
      "Reason:",
      "The indexed public summary does not adequately reflect the final judgment entered for the defendant and may create reputational harm by omitting the final disposition.",
      "",
      "Attached Support:",
      "Certified or archived judgment image showing final disposition.",
      "",
      "Source Language:",
      "\"Plaintiff failed to prove her claim.\"",
      "\"Enters judgment for Defendant.\""
    ].join("\n");
  },

  async copyBlockingRequest(currentUrl) {
    const text = this.buildBlockingRequest(currentUrl);
    await navigator.clipboard.writeText(text);
    return text;
  },

  openJustiaSupport() {
    window.open("https://support.justia.com/", "_blank", "noopener,noreferrer");
  },

  async handleJustiaBlockRequest(blockButton) {
    try {
      if (InputTools.isLoading) return;

      InputTools.isLoading = true;
      blockButton.classList.add("loading");

      const currentUrl = "https://law.justia.com/cases/vermont/superior-court/2026/22-st-00949.html";
      await this.copyBlockingRequest(currentUrl);
      this.openJustiaSupport();

      alert("Blocking request copied. Paste it into the Justia support request form.");
    } catch (error) {
      console.error("Justia blocking request error:", error);
      alert("Unable to prepare the Justia blocking request.");
    } finally {
      InputTools.isLoading = false;
      blockButton.classList.remove("loading");
    }
  }
};

function createJustiaBlockButton() {
  const btn = document.createElement("button");
  btn.type = "button";
  btn.className = "sl-button justia-block-button";
  btn.textContent = "Block Justia Link";
  btn.style.position = "fixed";
  btn.style.right = "20px";
  btn.style.bottom = "20px";
  btn.style.zIndex = "999999";
  btn.style.padding = "10px 14px";
  btn.style.cursor = "pointer";

  btn.addEventListener("click", () => JustiaTools.handleJustiaBlockRequest(btn));
  return btn;
}

function addJustiaBlockButton() {
  const target = document.body;
  if (!target) return;
  if (document.querySelector(".justia-block-button")) return;
  target.appendChild(createJustiaBlockButton());
}
'''

anchor = "slButtonLogic();\n  slRegisterListener();"

if anchor not in js:
    raise RuntimeError("Could not find the bottom call block. Patch manually.")

if "const JustiaTools =" in js:
    raise RuntimeError("JustiaTools block already exists. Not patching twice.")

patched = js.replace(
    anchor,
    injection + "\n\n  slButtonLogic();\n  slRegisterListener();\n  addJustiaBlockButton();",
    1
)

OUTPUT_PATH.write_text(patched, encoding="utf-8")

print(f"Patched file written to: {OUTPUT_PATH}")
print(json.dumps(report, indent=2))
