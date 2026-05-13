import streamlit as st

from pizza_chain import process_pizza_order
st.set_page_config(
    page_title="Pizza Order AI System",
    layout="centered"
)

st.title("Pizza Order AI System")

st.write("Order pizza using natural language!")

if "messages" not in st.session_state:

    st.session_state.messages = []

if "orders" not in st.session_state:

    st.session_state.orders = []

with st.sidebar:

    st.header("Pizza Menu")

    st.write("Chicken Pizza")
    st.write("Veggie Pizza")
    st.write("Paneer Pizza")
    st.write("Cheese Pizza")
    st.write("Chocolate Pizza")

    st.header("Sizes")

    st.write("Small")
    st.write("Medium")
    st.write("Large")

    if st.button("Clear Order"):

        st.session_state.messages = []
        st.session_state.orders = []

        st.rerun()
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_input = st.chat_input(
    "Example: I want one large chicken pizza"
)
if user_input:
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )
    with st.chat_message("user"):

        st.markdown(user_input)
    ai_response = process_pizza_order(
        user_input,
        st.session_state.orders
    )

    intent = ai_response.get("intent")

    reply = ai_response.get("confirmation_message")

    if not reply:

        reply = "Added your pizza to the order."
    if intent == "add_order":

        order_item = {
            "pizza_name": ai_response.get("pizza_name"),
            "size": ai_response.get("size"),
            "quantity": ai_response.get("quantity"),
            "toppings": ai_response.get("toppings") or []
        }

        st.session_state.orders.append(order_item)
    elif intent == "cancel_order":

        st.session_state.orders = []

        reply = "Your order has been cancelled."
    elif intent == "confirm_order":

        if st.session_state.orders:

            summary = "### Final Order Summary\n\n"

            for index, order in enumerate(
                st.session_state.orders,
                start=1
            ):

                toppings = order["toppings"]

                if toppings:

                    toppings_text = ", ".join(toppings)

                else:

                    toppings_text = "None"

                summary += f"""
**Item {index}**
- Pizza: {order["pizza_name"]}
- Size: {order["size"]}
- Quantity: {order["quantity"]}
- Toppings: {toppings_text}

"""

            reply = summary

        else:

            reply = "Your order is empty. Please add a pizza first."


    elif intent == "ask_missing_info":

        reply = ai_response.get("confirmation_message") or "Please provide pizza name, size, and quantity."


    elif intent == "general_question":

        reply = ai_response.get("confirmation_message") or "You can order Chicken, Veggie, Paneer, Cheese, or Chocolate Pizza."


    else:

        reply = "Sorry, I could not understand that. Please try again."


    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": reply
        }
    )

    
    with st.chat_message("assistant"):

        st.markdown(reply)
st.divider()

st.subheader("Current Order Memory")

if st.session_state.orders:

    for index, order in enumerate(
        st.session_state.orders,
        start=1
    ):

        st.write(
            f"""
**Item {index}:** {order["quantity"]} x {order["size"]} {order["pizza_name"]}
"""
        )

        if order["toppings"]:

            st.write(
                f"Toppings: {', '.join(order['toppings'])}"
            )

else:

    st.info("No pizza added yet.")