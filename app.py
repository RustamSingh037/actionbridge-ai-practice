
import streamlit as st
from agent import create_plan
from tools import save_note, list_notes

st.set_page_config(page_title="ActionBridge AI", page_icon="🤖")

st.title("🤖 ActionBridge AI")
st.caption("Turn natural-language requests into plans and verified actions.")

if "plan" not in st.session_state:
    st.session_state.plan = None

if "save_message" not in st.session_state:
    st.session_state.save_message = None

request = st.text_area(
    "What would you like me to help you do?",
    placeholder="Create a study plan for my ML exam and save it.",
    height=120,
)

if st.button("Create plan", type="primary"):
    if not request.strip():
        st.warning("Please enter a task.")
    else:
        try:
            with st.spinner("AI is planning..."):
                st.session_state.plan = create_plan(request)
            st.session_state.save_message = None
        except Exception as e:
            st.error(f"Planning failed: {e}")

plan = st.session_state.plan

if plan:
    st.subheader(plan["task"])
    st.write("### Proposed steps")

    for i, step in enumerate(plan["steps"], start=1):
        st.write(f"{i}. {step}")

    st.divider()
    st.write("### Approved action")
    st.caption("Save the plan as a note on this computer.")

    with st.form("save_plan_form"):
        confirm_save = st.form_submit_button("Save and verify plan")

    if confirm_save:
        try:
            content = "\n".join(
                f"{i}. {step}"
                for i, step in enumerate(plan["steps"], start=1)
            )
            result = save_note(plan["task"], content)

            if result.get("success") and result.get("verified"):
                st.session_state.save_message = (
                    "success",
                    f"Saved and verified: {result['file']}"
                )
            else:
                st.session_state.save_message = (
                    "error",
                    "The save could not be verified."
                )
        except Exception as e:
            st.session_state.save_message = ("error", str(e))

    if st.session_state.save_message:
        kind, message = st.session_state.save_message
        if kind == "success":
            st.success(message)
        else:
            st.error(f"Saving failed: {message}")

st.divider()
st.subheader("Saved notes")

try:
    notes = list_notes()

    if notes:
        for note in notes:
            with st.expander(note.get("title", "Untitled note")):
                st.write(note.get("content", ""))
    else:
        st.info("No notes saved yet.")
except Exception as e:
    st.error(f"Could not load saved notes: {e}")
