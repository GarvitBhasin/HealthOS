export function getToken() {
    const urlParams = new URLSearchParams(window.location.search);
    const token = urlParams.get('token');

    return token;
}