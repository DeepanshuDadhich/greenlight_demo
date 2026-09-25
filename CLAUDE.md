This is the Greenlight web app. It talks only to the Greenlight FastAPI backend (never to TrueForge directly), through Next.js server route handlers that attach the backend API key server side.

Greenlight takes any GitHub repo link, finds vulnerable dependencies, fixes them in a sandbox until tests pass, and opens a PR. If the bot account (greenlight-agent) is a collaborator on the repo, the user can choose "Ship it" (agent asks for approval, then merges) or "PR only". If the bot is not a collaborator, it forks and opens a PR, and there is no merge option.

The UI never fakes agent behaviour. Every state on screen comes from a real event streamed by the backend.

Rules:
1. Never expose API keys to the client.
2. Keep scope tight. Working beats pretty.
3. No hyphens in any user facing copy.

Design skills, each with one job:
1. design-taste-frontend: first build of each screen only.
2. Impeccable: owns PRODUCT.md and DESIGN.md. DESIGN.md wins on visual decisions. Fix its hook findings before moving on.
3. Emil Kowalski's skills: all motion. animate for every animation, pick-ui-library before installing UI packages, review-animations for audits.