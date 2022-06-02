# News_Portal
 SF Django News Portal Tutorial

As of D6 final task:

* В категории должна быть возможность пользователей подписываться на рассылку новых статей.

***Реализована подписка на категории (при выборе категории в списке постов) и, отдельно, на автора (при выборе автора в списке постов). Если пользователь уже подписан на данного автора и категорию, он об этом извещается и кнопка подписки меняется на кнопку отписки.***

****

* Если пользователь подписан на какую-либо категорию, то, как только в неё добавляется новая статья, её краткое содержание приходит пользователю на электронную почту, которую он указал при регистрации. В письме обязательно должна быть гиперссылка на саму статью, чтобы он мог по клику перейти и прочитать её.

***Письма приходят всем пользователям с емэйлом (отдельное письмо по каждой категории, даже если это один и тот же пост). При оформлении подписки на автора, пользователь с емэйлом тоже получает соответствующее письмо. Рассылка о выходе новых постов автора не реализована, но это нетрудно и тупо вопрос времени -- я катастрофически не успевал. Гиперссылки в письме и вотэтовотвсё реализовано (единственное - ссылка в письме идёт не на localhost, а на "реальный" веб-адрес, но это просто на будущее сделано, когда сей шедевр будет покорять тру-интернеты.***

****

* Если пользователь подписан на какую-либо категорию, то каждую неделю ему приходит на почту список новых статей, появившийся за неделю с гиперссылкой на них, чтобы пользователь мог перейти и прочесть любую из статей.

***Приходит... с божьей помощью и такой-то матери...***

****

* Добавьте приветственное письмо пользователю при регистрации в приложении.

***Сделано.***

З.Ы. Запускать отдельно планировщик через *манаге.пу* **НЕ НАДО!**
****

As of D4 final task:

* поиск с использованием виджета календаря реализован.
* В части разделения урлов на "новость" и "статья" -- я не вижу в этом никакой необходимости -- все посты это просто посты, нельзя сказать, что "новость" это не "статья" и что "статья" это не "новость".
* Выполнена фильтрация и пагинация: и на странице с постами, и на странице с поиском.
* Добавлено еще несколько дополнительных "плюшек", типа открытия отдельного поста кликом на заголовок (и на общей странице, и на странице с поиском).
* На странице с поиском указывается, сколько постов найдено по заданным критериям.