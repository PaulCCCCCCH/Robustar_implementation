<template>
  <div class="d-flex flex-column align-center">
    <v-card elevation="2" outlined class="my-8 pa-8">
      <v-card-title> <h2>Robustar Version: v0.2.0</h2> </v-card-title>
      <v-card-subtitle> Released: Jan 15, 2023 </v-card-subtitle>

      <!-- Resources -->
      <v-divider class="mt-4"></v-divider>

      <v-card-text>
        <h2 class="mb-2">Resources</h2>
        <v-btn
          text
          href="https://haohanwang.github.io/Robustar/"
          target="_blank"
          depressed
          color="primary"
        >
          Documentation and Tutorial
        </v-btn>
        <br />

        <v-btn
          text
          href="https://github.com/PaulCCCCCCH/Robustar_implementation"
          target="_blank"
          depressed
          color="primary"
        >
          Source Code
        </v-btn>
      </v-card-text>

      <!-- Bug report -->
      <v-divider class="mt-4"></v-divider>

      <v-card-text>
        <h2 class="mb-2">Saw a bug?</h2>

        <v-btn text href="mailto:chonghac@andrew.cmu.edu" target="_blank" depressed color="primary">
          Send us an email
        </v-btn>

        or
        <v-btn
          text
          href="https://github.com/PaulCCCCCCH/Robustar_implementation/issues/new"
          target="_blank"
          depressed
          color="primary"
        >
          Raise an issue here
        </v-btn>
      </v-card-text>

      <!-- More about us -->
      <v-divider class="mt-4"></v-divider>

      <v-card-text>
        <h2 class="mb-4">More about us</h2>
        We are a group of enthusiastic open-source contributors based off the USA, UK and China.
        <br />
        Follow us on:

        <v-btn class="mb-4" icon>
          <v-icon>mdi-github</v-icon>
        </v-btn>

        <v-btn class="mb-4" icon>
          <v-icon>mdi-twitter</v-icon>
        </v-btn>

        <v-btn class="mb-4" icon>
          <v-icon>mdi-instagram</v-icon>
        </v-btn>
      </v-card-text>
    </v-card>
  </div>
</template>

<script></script>

<style scoped></style>
