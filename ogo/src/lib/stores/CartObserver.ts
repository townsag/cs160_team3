import { writable } from "svelte/store";

// for state reactivity between components
// use with caution (can cause memory leaks if not unsubscribed properly)
export const cartItemQuantitySignal = writable(false);
export const cartItemRemovedSignal = writable(false);