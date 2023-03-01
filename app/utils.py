from bot_loader import bot


def html_mention(user_id, name='username'):
    return f'<a href=\"tg://user?id={user_id}\">{name}</a>'


async def user_mention(user_id, name='username', return_full_name_on_error=True):
    try:
        user_chat = await bot.get_chat(user_id)
        if user_chat.has_private_forwards and not user_chat.username:
            if return_full_name_on_error:
                return user_chat.full_name
            else:
                raise RuntimeError('User is not available for mention')
        else:
            return user_chat.get_mention(name=user_chat.mention or name, as_html=True)
    except Exception as e:
        if return_full_name_on_error:
            return html_mention(user_id, name)
        else:
            raise RuntimeError('User is not available for mention')
