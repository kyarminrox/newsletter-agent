# SubstackAssistant v1

SubstackAssistant v1 is a command-line tool (and optional web interface) that helps generate a brief and a Markdown draft for your next Substack post. The assistant processes summaries of your previous posts, engagement metrics, and reader comments to suggest a data-driven topic, hooks, and structure.

## Usage

1. Prepare an input JSON file (see `example_input.json`) that includes summaries of your latest posts, engagement metrics, top comment excerpts, any additional keyword research, and your objective for the next post.
2. Run the assistant:

```bash
python3 substack_assistant.py example_input.json > output.json
```

3. The script outputs a JSON object with the following fields:

- `brief` – topic recommendation, outline, hooks, and personas addressed.
- `draft_markdown` – a ready-to-use Markdown draft for Substack.
- `optimization_notes` – suggestions for send time, preview text, images or links, and subject line tests.
- `next_steps_checklist` – step-by-step instructions to finalize and schedule the post.

You can copy the generated Markdown into Substack and follow the checklist to complete your post.

## Web Front-End

An example Next.js interface is included in the `next-app` directory. It lets you provide your Groq API key and JSON input to generate a post via the Groq API.

To start the interface locally (after installing dependencies):

```bash
cd next-app
npm install # requires internet access
npm run dev
```

Then open <http://localhost:3000> in your browser and submit the form.

## License

This project is licensed under the GNU General Public License v3.0. See the `LICENSE` file for details.
